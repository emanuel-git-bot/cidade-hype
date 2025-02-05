from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RobloxUser
from django.utils import timezone

@api_view(['POST'])
def register_user(request):
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    
    if not user_id or not username:
        return Response({
            'error': 'ID do Roblox e nome de usuário são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se o usuário já existe
    if RobloxUser.objects.filter(user_id=user_id).exists():
        return Response({
            'user_id': 'Este ID do Roblox já está cadastrado'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Cria o novo usuário
    user = RobloxUser.objects.create(
        user_id=user_id,
        username=username,
        last_login=timezone.now()
    )
    
    return Response({
        'message': 'Usuário cadastrado com sucesso',
        'user_id': user.user_id,
        'username': user.username
    }, status=status.HTTP_201_CREATED) 