from django.contrib import admin
from .models import BugReport

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at', 'resolved_at')
    search_fields = ('title', 'description', 'resolution_notes')
    readonly_fields = ('created_at', 'resolved_at')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        for bug in queryset:
            if bug.status == 'pending':
                bug.resolve()
    mark_as_resolved.short_description = "Marcar bugs selecionados como resolvidos" 