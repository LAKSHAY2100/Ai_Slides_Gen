from django.urls import path
from .views import *

urlpatterns = [
    path('', slide_builder, name='slide_builder'),
    path('api/generate_slides/',generate_slides,name='generate_slides')
]
