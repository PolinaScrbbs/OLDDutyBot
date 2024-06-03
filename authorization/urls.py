from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView, LoginView, UsersView 

urlpatterns = [
    path('signup/', SignupView.as_view(), name='auth-signup'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('users/', UsersView.as_view(), name='users'),
    path('users/<int:pk>/', UsersView.as_view(), name='user-detail'),
    path('token-refresh/', TokenRefreshView.as_view)
]