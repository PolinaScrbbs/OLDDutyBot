from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from authorization.models import User, TokenAuthentication
from .models import Duty
from .serializers import AttendantSerializer, DutyDetailSerializer, DutyCountSerializer
from datetime import datetime

class DutyListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        group = user.group

        duties = Duty.objects.filter(attendant__group=group).order_by('attendant__full_name', 'date')
        if duties.__len__() == 0:
            return Response({"message": f"Список дежурств группы {group} пуст"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DutyDetailSerializer(duties, many=True)
        return Response({f"duties": serializer.data})
    
    def post(self, request):
        user = request.user
        if user.role.id not in [1,2]:
            return Response({"error": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)
        attendants = request.data.get("attendants")
        try:
            for attendant in attendants:
                attendant = User.objects.get(id=attendant['id'])

                if attendant.group != user.group:
                    return Response({"error": f"Студент {attendant.full_name} из группы {attendant.group}, а не из вашей {user.group}"}, status=status.HTTP_400_BAD_REQUEST)
                
                Duty.objects.create(attendant=attendant)

            return Response({"message": "Duties created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({f"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DutyCountListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        group = user.group

        duties = Duty.objects.filter(attendant__group=group).order_by('attendant__full_name', 'date')
        if duties.__len__() == 0:
            return Response({"message": f"Список дежурств группы {group} пуст"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DutyCountSerializer(duties, many=True)
        return Response({f"duties": serializer.data})


# Получение двух людей с наименьшей датой последнего дежурства из заданного списка
def get_min_date_attendant(attendant_list):
    min_attendant = []
    null_date = datetime.strptime('2023-12-04', '%Y-%m-%d').date()

    for attendant in attendant_list:
        if attendant['last_duty_date'] is not None:
            last_duty_date = attendant['last_duty_date']
        else:
            last_duty_date = null_date

        if len(min_attendant) < 2:
            min_attendant.append((attendant, last_duty_date))

        else:
            min_attendant.sort(key=lambda x: x[1])
            if last_duty_date < min_attendant[1][1]:
                min_attendant.pop()
                min_attendant.append((attendant, last_duty_date))

    return [attendant for attendant, _ in min_attendant]

class AttendantView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role.id not in [1, 2]:
            return Response({"error": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

        pass_attendant = request.data.get("pass_attendant")
        print(pass_attendant)

        attendant_list = User.objects.filter(group=user.group).order_by('full_name')

        if pass_attendant:
            pass_attendant_ids = list(map(int, pass_attendant))
            attendant_list = attendant_list.exclude(id__in=pass_attendant_ids)

        serialized_attendants = AttendantSerializer(attendant_list, many=True).data

        duties_counts = [attendant['duties_count'] for attendant in serialized_attendants]

        if all(count == duties_counts[0] for count in duties_counts):
            attendants = get_min_date_attendant(serialized_attendants)
            return Response({"attendants": attendants})
        else:
            min_duties_attendant = []
            min_duties = [min(duties_counts)]
            attendant_with_min_duties = 0
            for attendant in serialized_attendants:
                if attendant['duties_count'] in min_duties:
                    attendant_with_min_duties += 1
            if attendant_with_min_duties < 2:
                min_duties.append(min_duties[0] + 1)
            for attendant in serialized_attendants:
                if attendant['duties_count'] in min_duties:
                    min_duties_attendant.append(attendant)
            if len(min_duties_attendant) == 2:
                print(min_duties_attendant)
                return Response({"attendants": AttendantSerializer(min_duties_attendant, many=True).data})
            else:
                attendants = get_min_date_attendant(min_duties_attendant)
                print(attendants)
                return Response({"attendants": AttendantSerializer(attendants, many=True).data})

