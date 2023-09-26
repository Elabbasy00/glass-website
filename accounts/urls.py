from django.contrib import admin
from django.urls import path
from .views import *

app_name="accounts"

urlpatterns = [
    
     path('activate/', user_active, name='user_active'),
     path('re_activate', resend_active_code, name='re_activate'),
     path('profile/', profile, name='profile'),
     path('delete_address/<int:id>/', delete_address, name="delete_address"),
     path('default_address/<int:id>/', default_address, name="default_address")


]    










