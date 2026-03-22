from django.urls import path,include
from .views import *

urlpatterns=[
    path('',login_view,name='login'),
    path('register/',register_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard_view,name='dashboard'),
    path('accounts/', include('allauth.urls'),name='social_accounts'),
]