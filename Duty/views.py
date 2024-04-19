from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound

from .models import People, Duty
from .serializers import PeopleSerializer, DutySerializer

from datetime import datetime, date

class PeopleListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        people = People.objects.filter(group=user.group).order_by('full_name')
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)

class DutyListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        duties = Duty.objects.all()
        serializer = DutySerializer(duties, many=True)
        return Response(serializer.data)


# Получение двух людей с наименьшей датой последнего дежурства из заданного списка
def get_min_date_people(people_list):
    min_people = []
    null_date = datetime.strptime('2023-12-04', '%Y-%m-%d').date()

    for person in people_list:
        if person.last_duty_date is not None:
            last_duty_date = person.last_duty_date
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

        pass_people = request.data.get("pass_people")
        people_list = People.objects.filter(group=user.group).order_by('full_name')

        if pass_people:
            people_list = people_list.exclude(id__in=pass_people)

        people_duties_count = [people.duties_count for people in people_list]

        if all(person_duties_count == people_duties_count[0] for person_duties_count in people_duties_count):
            attendants = get_min_date_people(people_list)
            return Response(PeopleSerializer(attendants, many=True).data)
        else:
            min_duties_people = []
            min_duties = [min(people_duties_count)]
            people_with_min_duties = 0
            for people in people_list:
                if people.duties_count in min_duties:
                    people_with_min_duties += 1
            if people_with_min_duties < 2:
                min_duties.append(min_duties[0]+1)
            for people in people_list:
                if people.duties_count in min_duties:
                    min_duties_people.append(people)
            if len(min_duties_people) == 2:
                return Response(PeopleSerializer(min_duties_people, many=True).data)
            else:
                attendants = get_min_date_people(min_duties_people)
                return Response(PeopleSerializer(attendants, many=True).data)

