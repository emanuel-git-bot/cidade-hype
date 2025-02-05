from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('api/users/register/', views.register_user, name='register'),
] 