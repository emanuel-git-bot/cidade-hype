from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('api/events/', views.list_events, name='list_events'),
    path('api/events/<int:event_id>/', views.get_event, name='get_event'),
] 