from django.urls import path
from .views import AttendantView, DutyListView, DutyCountListView

urlpatterns = [
    path('attendants/', AttendantView.as_view(), name='get-attendant'),
    path('duties/', DutyListView.as_view(), name='duty-detail'),
    path('duties_count/', DutyCountListView.as_view(), name='duty-detail'),
]

