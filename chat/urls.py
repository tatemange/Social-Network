from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/private/<int:user_id>/', views.get_or_create_private_chat, name='get_or_create_private_chat'),
    path('chat/group/create/', views.create_group_chat, name='create_group_chat'),
    path('chat/room/<int:discussion_id>/', views.chat_room, name='chat_room'),
]
