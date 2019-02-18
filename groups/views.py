from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions

from django.contrib.auth.models import Group

from .serializers import GroupSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
