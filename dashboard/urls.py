from django.urls import path
from .views import dashboard, settings, sensor_names
urlpatterns=[
	path('', dashboard),
	path('settings/', settings, name='settings'),
	path('sensor-names/', sensor_names, name='sensor_names'),
]
