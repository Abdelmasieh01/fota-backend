from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import UserDetailsSerializer

# Create your views here.


class UserDetails(RetrieveAPIView):
    serializer_class = UserDetailsSerializer

    def get_object(self):
        if self.request.user.is_active:
            return self.request.user
        return None
    
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            return super().retrieve(request, *args, **kwargs)
        return Response(data={'message': 'Unauthenticated user!'}, status=status.HTTP_401_UNAUTHORIZED)