from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'title', 'description', 'screenshot', 'status',
                 'created_at', 'resolved_at', 'resolution_notes']
        read_only_fields = ['status', 'resolved_at', 'resolution_notes']

class BugReportAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'title', 'description', 'screenshot', 'status',
                 'created_at', 'resolved_at', 'resolution_notes'] 