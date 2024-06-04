from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from authorization.models import User, TokenAuthentication
from .models import Duty
from .serializers import AttendantSerializer, DutyDetailSerializer
from datetime import datetime

# class PeopleListView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         people = People.objects.filter(group=user.group).order_by('full_name')
#         serializer = PeopleSerializer(people, many=True)
#         return Response(serializer.data)

class DutyListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        group = user.group

        duties = Duty.objects.filter(duty__group=group).order_by('duty__full_name', 'date')
        if duties.__len__() == 0:
            return Response({"message": f"Список дежурств группы {group} пуст"})
        
        serializer = DutyDetailSerializer(duties, many=True)
        return Response({f"Дежурства группы {group}": serializer.data})
    
    def post(self, request):
        user = request.user
        if user.role.id not in [1,2]:
            return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)
        duties = request.data.get("duties")
        try:
            for duty in duties:
                duty = User.objects.get(full_name=duty)

                if duty.group != user.group:
                    return Response({"error": f"Студент {duty.full_name} из группы {duty.group}, а из вашей {user.group}"}, status=status.HTTP_400_BAD_REQUEST)
                
                Duty.objects.create(duty=duty)

            return Response({"message": "Duties created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({f"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Получение двух людей с наименьшей датой последнего дежурства из заданного списка
def get_min_date_people(people_list):
    min_people = []
    null_date = datetime.strptime('2023-12-04', '%Y-%m-%d').date()

    for person in people_list:
        if person['last_duty_date'] is not None:
            last_duty_date = person['last_duty_date']
        else:
            last_duty_date = null_date

        if len(min_people) < 2:
            min_people.append((person, last_duty_date))

        else:
            min_people.sort(key=lambda x: x[1])
            if last_duty_date < min_people[1][1]:
                min_people.pop()
                min_people.append((person, last_duty_date))

    return [person for person, _ in min_people]

class AttendantView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role.id not in [1,2]:
            return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

        pass_attendant = request.data.get("pass_people")
        attendant_list = User.objects.filter(group=user.group).order_by('full_name')

        if pass_attendant:
            attendant_list = attendant_list.exclude(id__in=attendant_list)

        serialized_attendants = AttendantSerializer(attendant_list, many=True).data

        attendant_duties_count = [attendant['duties_count'] for attendant in serialized_attendants]
        print(attendant_duties_count)

        if all(person_duties_count == attendant_duties_count[0] for person_duties_count in attendant_duties_count):
            attendants = get_min_date_people(serialized_attendants)
            return Response({"Дежурные": attendants})
        else:
            min_duties_people = []
            min_duties = [min(attendant_duties_count)]
            people_with_min_duties = 0
            for people in serialized_attendants:
                if people['duties_count'] in min_duties:
                    people_with_min_duties += 1
            if people_with_min_duties < 2:
                min_duties.append(min_duties[0]+1)
            for people in serialized_attendants:
                if people['duties_count'] in min_duties:
                    min_duties_people.append(people)
            if len(min_duties_people) == 2:
                return Response(AttendantSerializer(min_duties_people, many=True).data)
            else:
                attendants = get_min_date_people(min_duties_people)
                return Response(AttendantSerializer(attendants, many=True).data)

