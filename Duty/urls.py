from django.urls import path
from .views import PeopleListView, PeopleDetailView, DutyListView, DutyDetailView

urlpatterns = [
    path('people/', PeopleListView.as_view({'get': 'list', 'post': 'create'}), name='people-list'),
    path('people/<int:pk>/', PeopleDetailView.as_view(), name='people-detail'),
    path('duties/', DutyListView.as_view({'get': 'list', 'post': 'create'}), name='duty-list'),
    path('duties/<int:pk>/', DutyDetailView.as_view(), name='duty-detail'),
]

