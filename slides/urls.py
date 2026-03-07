from django.urls import path
from .views import *

urlpatterns = [
    path('', slide_builder, name='slide_builder'),
    path('api/generate_slides/',generate_slides,name='generate_slides'),
    path('api/share/',share_slides,name='share_slides'),
    path('view/<str:code>/',view_shared,name='share_slides'),   
]
