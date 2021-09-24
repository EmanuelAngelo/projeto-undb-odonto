from user.forms import PasswordChangeForm
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from user.models import Usuario
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from gdbundbrm.custom_views import RMCustomGenericAPIView, RMCustomRetrieveUpdateDestroyAPIView
# Create your views here.

class UserAPIView(RMCustomGenericAPIView):

    def post(self, request, *args, **kwargs):  #usar para mudar senha do usuario
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        try:
            u = Usuario.objects.get(username=username)
            valida = check_password(password, u.token)
            stat = status.HTTP_200_OK if valida else status.HTTP_401_UNAUTHORIZED
            if valida:
                serial_user = UserSerializer(u).data
            else:
                serial_user = None
            return Response(serial_user, status=stat)
        except:
            stat = status.HTTP_404_NOT_FOUND
            return Response(None,  status=stat)


class UserUpdateTokenAPIView(RMCustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        usuario = self.request.data.get('usuario', None)
        password = self.request.data.get('password', None)
        if password and usuario:
            if len(password) < 6:
                raise serializers.ValidationError('Quantidade mínima de 6 caracteres.')
            try:
                user = Usuario.objects.get(username=usuario)
                user.token = make_password(password)
                user.save()
            except:
                raise serializers.ValidationError('Usuário não encontrado.')
        else:
            raise serializers.ValidationError('Usuário e/ou Senha não informados.')

        return Response(None, status=200)