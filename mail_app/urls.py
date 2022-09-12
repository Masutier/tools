from django.urls import path, include
from .views import *


urlpatterns = [
    path('mailTool', mailTool, name="mailTool"),
    path('mailSend', mailSend, name="mailSend"),

]
