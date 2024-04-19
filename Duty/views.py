from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from .models import People, Duty
from .serializers import PeopleSerializer, DutySerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response


class PeopleListView(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

    def check_token(self, request):
        token_key = request.GET.get('token')
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    def get_queryset(self):
        user = self.check_token(self.request)
        if not user:
            return People.objects.none()  # Возвращаем пустой QuerySet, если токен недействителен

        return People.objects.filter(group=user.group).order_by('full_name')

    def create(self, request, *args, **kwargs):
        user = self.check_token(request)
        if not user:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.check_token(request)
        if not user:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.check_token(request)
        if not user:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().destroy(request, *args, **kwargs)

class PeopleDetailView(RetrieveAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

class DutyListView(viewsets.ModelViewSet):
    queryset = Duty.objects.all()
    serializer_class = DutySerializer

class DutyDetailView(RetrieveAPIView):
    queryset = Duty.objects.all()
    serializer_class = DutySerializer

