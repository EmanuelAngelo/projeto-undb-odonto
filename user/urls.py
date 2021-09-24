from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'user'

urlpatterns = [
    path('api/v1/validate-password/', views.UserAPIView.as_view(), name='api_validate_password'),
    path('update-token/', views.UserUpdateTokenAPIView.as_view(), name='update_token'),

]