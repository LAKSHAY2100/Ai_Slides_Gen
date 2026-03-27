from django.urls import path , include
from .views import *

urlpatterns = [
    path('', story_telling, name='home'),
    path('slides/', slide_builder, name='slide_builder'),
    path('api/generate_slides/',generate_slides,name='generate_slides'),
    path('api/share/',share_slides,name='share_slides'),
    path('view/<str:code>/',view_shared,name='view_slides'),   
    path('story/', story_telling , name='story_telling'),
    path('auth/', include('auth_app.urls')),
]
