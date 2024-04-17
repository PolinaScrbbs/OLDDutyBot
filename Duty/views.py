from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from .models import People, Duty
from .serializers import PeopleSerializer, DutySerializer

class PeopleListView(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

class PeopleDetailView(RetrieveAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

class DutyListView(viewsets.ModelViewSet):
    queryset = Duty.objects.all()
    serializer_class = DutySerializer

class DutyDetailView(RetrieveAPIView):
    queryset = Duty.objects.all()
    serializer_class = DutySerializer

