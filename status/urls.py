from django.urls import path
from . import views

app_name = 'status'

urlpatterns = [
    path('feed/', views.get_status_feed, name='feed'),
    path('add/', views.add_status, name='add_status'),
]
