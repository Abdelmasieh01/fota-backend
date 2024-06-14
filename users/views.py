from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from datetime import datetime
import pytz

from .serializers import UserDetailsSerializer

from .models import EmailConfirmationToken

from .utils import send_confirmation_email


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


class SendEmailConfirmationTokenAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        if user.is_email_confirmed:
            return Response(data={"message": "Already confirmed!"}, status=400)
        token = EmailConfirmationToken.objects.create(user=user)
        print(request.get_host())
        send_confirmation_email(
            email=user.email, token_id=token.pk, user_id=user.pk, host=request.get_host())
        return Response(data=None, status=201)


def confirm_email_view(request):
    token_id = request.GET.get("token_id", None)
    user_id = request.GET.get("user_id", None)
    if user_id is None or token_id is None:
        print("test")
        return HttpResponseNotFound()
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        timestamp = token.created_at
        now = datetime.now().astimezone(timestamp.tzinfo)
        differnce = (now - timestamp).seconds / 60
        if differnce > 30:
            raise ValueError
        token.delete()
        context = {"is_email_confirmed": True}
    except EmailConfirmationToken.DoesNotExist:
        context = {'is_email_confirmed': False}
    except ValueError:
        token.delete()
        context = {'is_email_confirmed': False}
    return render(request, "users/confirm_email.html", context)
