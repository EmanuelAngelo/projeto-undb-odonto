from django.urls import path, include
from base.views import PageLoginView, IndexView

app_name = 'base'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login/', PageLoginView.as_view(), name='login'),
   
]
