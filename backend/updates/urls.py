from django.urls import path
from . import views

app_name = 'updates'

urlpatterns = [
    path('api/updates/', views.list_updates, name='list_updates'),
    path('api/coming-soon/', views.list_coming_soon, name='list_coming_soon'),
] 