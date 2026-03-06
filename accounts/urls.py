from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Contact API
    path('contact/add/<int:user_id>/', views.add_contact, name='add_contact'),
    path('contact/add_by_phone/', views.add_contact_by_phone, name='add_contact_by_phone'),
    path('contact/block/<int:user_id>/', views.block_contact, name='block_contact'),
]
