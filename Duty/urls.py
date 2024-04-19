from django.urls import path
from .views import PeopleListView, AttendantView, DutyListView

urlpatterns = [
    path('people/', PeopleListView.as_view(), name='people-list'),
    path('attendant/', AttendantView.as_view(), name='get-attendant'),
    path('duties/', DutyListView.as_view(), name='duty-detail'),
]

