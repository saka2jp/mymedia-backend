from rest_framework import generics, permissions

from django.contrib.auth.models import Group

from .serializers import GroupSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
