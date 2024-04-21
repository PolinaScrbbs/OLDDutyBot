from django.contrib.auth import authenticate

from .models import Admin
from .serializers import AdminSerializer

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .functions import get_admin_by_token

#Получение и добавление пользователей
class AdminsView(ListCreateAPIView):
    serializer_class = AdminSerializer

    def get(self, request):
        token = request.GET.get('token', None)
        admin = get_admin_by_token(token)
        serializer = self.get_serializer(admin)
        return Response({"Пользователь": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Создан пользователь": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Авторизация и создание токена
class LoginView(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        print(login, password)

        admin = authenticate(request, full_name=login, password=password)

        if admin:
            token, _ = Token.objects.get_or_create(user=admin)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)
