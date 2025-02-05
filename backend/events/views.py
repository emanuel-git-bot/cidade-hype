from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event, EventImage, EventLink
from django.utils import timezone

@api_view(['GET'])
def list_events(request):
    status_filter = request.query_params.get('status')
    events = Event.objects.all()
    
    if status_filter:
        events = events.filter(status=status_filter)
    
    data = [{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'status': event.status,
        'start_date': event.start_date,
        'end_date': event.end_date,
        'images': [{
            'id': image.id,
            'url': request.build_absolute_uri(image.image.url)
        } for image in event.images.all()],
        'links': [{
            'id': link.id,
            'title': link.title,
            'url': link.url
        } for link in event.links.all()]
    } for event in events]
    return Response(data)

@api_view(['GET'])
def get_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({
            'error': 'Evento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'status': event.status,
        'start_date': event.start_date,
        'end_date': event.end_date,
        'images': [{
            'id': image.id,
            'url': request.build_absolute_uri(image.image.url)
        } for image in event.images.all()],
        'links': [{
            'id': link.id,
            'title': link.title,
            'url': link.url
        } for link in event.links.all()]
    }
    return Response(data) 