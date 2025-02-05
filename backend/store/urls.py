from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # URLs para templates
    path('painel/', views.dashboard, name='dashboard'),
    path('painel/categories/', views.category_list, name='category_list'),
    path('painel/categories/create/', views.category_create, name='category_create'),
    path('painel/categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('painel/categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    
    path('painel/items/', views.item_list, name='item_list'),
    path('painel/items/create/', views.item_create, name='item_create'),
    path('painel/items/<int:item_id>/edit/', views.item_edit, name='item_edit'),
    path('painel/items/<int:item_id>/delete/', views.item_delete, name='item_delete'),
    
    path('painel/bugs/', views.bug_list, name='bug_list'),
    path('painel/bugs/<int:bug_id>/', views.bug_detail, name='bug_detail'),
    
    # URLs para Atualizações
    path('painel/updates/', views.update_list, name='update_list'),
    path('painel/updates/create/', views.update_create, name='update_create'),
    path('painel/updates/<int:update_id>/edit/', views.update_edit, name='update_edit'),
    path('painel/updates/<int:update_id>/delete/', views.update_delete, name='update_delete'),
    path('painel/updates/image/<int:image_id>/delete/', views.update_image_delete, name='update_image_delete'),
    
    # URLs para Eventos
    path('painel/events/', views.event_list, name='event_list'),
    path('painel/events/create/', views.event_create, name='event_create'),
    path('painel/events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('painel/events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('painel/events/image/<int:image_id>/delete/', views.event_image_delete, name='event_image_delete'),
    
    # URLs para Em Breve
    path('painel/comingsoon/', views.comingsoon_list, name='comingsoon_list'),
    path('painel/comingsoon/create/', views.comingsoon_create, name='comingsoon_create'),
    path('painel/comingsoon/<int:item_id>/edit/', views.comingsoon_edit, name='comingsoon_edit'),
    path('painel/comingsoon/<int:item_id>/delete/', views.comingsoon_delete, name='comingsoon_delete'),
    path('painel/comingsoon/image/<int:image_id>/delete/', views.comingsoon_image_delete, name='comingsoon_image_delete'),
    
    # URLs para API
    path('api/categories/', views.list_categories, name='list_categories'),
    path('api/items/', views.list_items, name='list_items'),
    path('api/orders/', views.list_orders, name='list_orders'),
    path('api/orders/create/', views.create_order, name='create_order'),
    path('api/bugs/report/', views.report_bug, name='report_bug'),
    
    # API Endpoints
    path('api/updates/', views.update_list_api, name='update_list_api'),
    path('api/events/', views.event_list_api, name='event_list_api'),
    path('api/comingsoon/', views.comingsoon_list_api, name='comingsoon_list_api'),
] 