from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bugs', views.BugReportViewSet)

app_name = 'bugs'

urlpatterns = [
    path('api/', include(router.urls)),
] 