from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import BugReport
from .serializers import BugReportSerializer, BugReportAdminSerializer

class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return BugReportAdminSerializer
        return BugReportSerializer

    def get_queryset(self):
        queryset = BugReport.objects.all()
        if not self.request.user.is_staff:
            # Usuários normais só veem bugs pendentes
            queryset = queryset.filter(status='pending')
        return queryset

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'Apenas administradores podem resolver bugs.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        bug = self.get_object()
        if bug.status != 'pending':
            return Response(
                {'error': 'Este bug já foi resolvido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        notes = request.data.get('notes', '')
        bug.resolve(notes=notes)
        
        serializer = self.get_serializer(bug)
        return Response(serializer.data) 