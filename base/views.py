from django.shortcuts import render
from django.contrib.auth.views import LoginView
from gdbundbrm.mixins import RMCheckPermissionMixin
from django.views.generic import TemplateView

class IndexView( RMCheckPermissionMixin, TemplateView):
    template_name="base/index.html"
    required_permission = False

class PageLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True