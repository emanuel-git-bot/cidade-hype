from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Update, UpdateImage, ComingSoon, ComingSoonImage

@api_view(['GET'])
def list_updates(request):
    updates = Update.objects.all()
    data = [{
        'id': update.id,
        'title': update.title,
        'description': update.description,
        'created_at': update.created_at,
        'images': [{
            'id': image.id,
            'url': request.build_absolute_uri(image.image.url)
        } for image in update.images.all()]
    } for update in updates]
    return Response(data)

@api_view(['GET'])
def list_coming_soon(request):
    coming_soon_items = ComingSoon.objects.all()
    data = [{
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'created_at': item.created_at,
        'images': [{
            'id': image.id,
            'url': request.build_absolute_uri(image.image.url)
        } for image in item.images.all()]
    } for item in coming_soon_items]
    return Response(data) 