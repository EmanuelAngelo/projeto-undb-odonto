from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'box'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('teste-email/', views.TesteEmailView.as_view(), name='teste_email'), #testar email ver template
    path('api/v1/caixas/', views.BoxAPIView.as_view(), name='api_caixas'),
    path('api/v1/situacao/', views.SituacaoAPIView.as_view(), name='api_situacao'),
    path('api/v1/deposito/', views.DepositoAPIView.as_view(), name='api_deposito'),
    path('api/v1/deposito/<pk>/', views.RUDDepositoAPIView.as_view(), name='rud_api_deposito'),
    path('api/v1/depositoitem/', views.DepositoItemAPIView.as_view(), name='api_depositoitem'),
    path('api/v1/depositoitem/<pk>/<method>/', views.RUDDepositoItemAPIView.as_view(), name='rud_api_depositoitem'),
    
]