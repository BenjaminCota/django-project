from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
