from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import AdminsView, LoginView

#Auth
urlpatterns = [
    path('signup/', AdminsView.as_view(), name='auth-signup'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('token-refresh/', TokenRefreshView.as_view)
]