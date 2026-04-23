from django.urls import path
from .views import dashboard, settings
urlpatterns=[path('',dashboard),path('settings/',settings,name='settings')]
