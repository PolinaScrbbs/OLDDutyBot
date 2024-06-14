from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from authorization.parser import get_group_list
from .models import Role, User, Token, TokenAuthentication
from .serializers import UserCreateSerializer, UserDetailSerializer

class SignupView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Создан пользователь": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')

        user = User.objects.get(username=login)
        is_password_correct = check_password(password, user.password)

        if is_password_correct:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)

class UsersView(CreateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_id = kwargs.get('pk')

        if user_id is not None:
            user_id = int(user_id)
            if user.role.id == 1 or user.id == user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    serializer = self.get_serializer(user)
                    return Response({"Пользователь": serializer.data})
                except User.DoesNotExist:
                    return Response({"Ошибка": "Пользователь с указанным ID не найден"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

        role_id = request.data.get("role_id")

        if role_id is not None:
            if user.role.id == 1:
                try:
                    role = Role.objects.get(id=role_id)
                    users = User.objects.filter(role=role).order_by('full_name')

                    if users.exists():
                        serializer = self.get_serializer(users, many=True)
                        return Response({f"Пользователи с ролью {role.title}": serializer.data})
                    else:
                        return Response({f"Пользователи с ролью {role.title} не найдены"}, status=status.HTTP_404_NOT_FOUND)
                except Role.DoesNotExist:
                    return Response({"Ошибка": "Роль с указанным ID не найдена"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

        group = request.data.get("group")

        if group is not None:
            if user.role.id in [1, 2]:
                group = group.upper()
                group_list = get_group_list()

                if group not in group_list:
                    return Response({"Ошибка": f"Группа {group} не найдена"}, status=status.HTTP_404_NOT_FOUND)

                if user.group != group and user.role.id != 1:
                    return Response({"Ошибка": "Отказано в доступе к другой группе"}, status=status.HTTP_403_FORBIDDEN)
                
                users = User.objects.filter(group=group).order_by('full_name')
                if users.exists():
                    serializer = self.get_serializer(users, many=True)
                    return Response({f"Пользователи с группой {group}": serializer.data})
                else:
                    return Response({f"Пользователи с группой {group} не найдены"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

        if user.role.id == 1:
            users = User.objects.all().order_by('full_name')
            if users.exists():
                serializer = self.get_serializer(users, many=True)
                return Response({"Пользователи": serializer.data})
            else:
                return Response({"Пользователи не найдены"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Ошибка": "Вы не имеете прав"}, status=status.HTTP_403_FORBIDDEN)

            
    

