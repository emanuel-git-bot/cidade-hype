from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Item, Order, Bug, Update, UpdateImage, UpdateLink, Event, EventImage, ComingSoon, ComingSoonImage
from django.utils import timezone
from django.http import JsonResponse

# Views baseadas em templates
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        icon = request.POST.get('icon')
        
        if Category.objects.filter(slug=slug).exists():
            messages.error(request, 'Já existe uma categoria com este slug.')
            return redirect('store:category_list')
        
        Category.objects.create(name=name, slug=slug, icon=icon)
        messages.success(request, 'Categoria criada com sucesso!')
        return redirect('store:category_list')
    
    return redirect('store:category_list')

def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug') or slugify(category.name)
        category.icon = request.POST.get('icon')
        
        if Category.objects.filter(slug=category.slug).exclude(id=category_id).exists():
            messages.error(request, 'Já existe uma categoria com este slug.')
        else:
            category.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
        
        return redirect('store:category_list')
    
    return render(request, 'store/category_edit.html', {'category': category})

def category_delete(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        try:
            category.delete()
            messages.success(request, 'Categoria excluída com sucesso!')
        except:
            messages.error(request, 'Não é possível excluir esta categoria pois existem itens vinculados a ela.')
    return redirect('store:category_list')

def dashboard(request):
    categories_count = Category.objects.count()
    items_count = Item.objects.count()
    orders_count = Order.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'categories_count': categories_count,
        'items_count': items_count,
        'orders_count': orders_count,
        'recent_orders': recent_orders
    }
    return render(request, 'store/dashboard.html', context)

# Views da API
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    data = [{
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'icon': category.icon
    } for category in categories]
    return Response(data)

@api_view(['GET'])
def list_items(request):
    category_id = request.query_params.get('category')
    items = Item.objects.all()
    if category_id:
        items = items.filter(category_id=category_id)
    
    data = [{
        'id': item.id,
        'category': {
            'id': item.category.id,
            'name': item.category.name
        },
        'name': item.name,
        'description': item.description,
        'price': str(item.price),
        'image': request.build_absolute_uri(item.image.url) if item.image else None,
        'observation': item.observation
    } for item in items]
    return Response(data)

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    item_id = request.data.get('item_id')
    
    if not all([user_id, username, item_id]):
        return Response({
            'error': 'Todos os campos são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({
            'error': 'Item não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    order = Order.objects.create(
        user_id=user_id,
        username=username,
        item=item,
        status='pending'
    )
    
    return Response({
        'message': 'Pedido criado com sucesso',
        'order_id': order.id,
        'status': order.status
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_orders(request):
    user_id = request.query_params.get('user_id')
    orders = Order.objects.all()
    if user_id:
        orders = orders.filter(user_id=user_id)
    
    data = [{
        'id': order.id,
        'user_id': order.user_id,
        'username': order.username,
        'item': {
            'id': order.item.id,
            'name': order.item.name,
            'price': str(order.item.price)
        },
        'status': order.status,
        'created_at': order.created_at,
        'delivered_at': order.delivered_at
    } for order in orders]
    return Response(data)

def item_list(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/item_list.html', {
        'items': items,
        'categories': categories
    })

def item_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        observation = request.POST.get('observation')
        image = request.FILES.get('image')
        
        try:
            category = Category.objects.get(id=category_id)
            Item.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                observation=observation,
                image=image
            )
            messages.success(request, 'Item criado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar item: {str(e)}')
        
        return redirect('store:item_list')
    
    return redirect('store:item_list')

def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.category_id = request.POST.get('category')
        item.observation = request.POST.get('observation')
        
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        
        try:
            item.save()
            messages.success(request, 'Item atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar item: {str(e)}')
        
        return redirect('store:item_list')
    
    return render(request, 'store/item_edit.html', {
        'item': item,
        'categories': categories
    })

def item_delete(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        try:
            item.delete()
            messages.success(request, 'Item excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir item: {str(e)}')
    return redirect('store:item_list')

def bug_list(request):
    bugs = Bug.objects.all()
    return render(request, 'store/bug_list.html', {'bugs': bugs})

def bug_detail(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            bug.status = request.POST.get('status')
            bug.save()
            messages.success(request, 'Status atualizado com sucesso!')
        
        elif action == 'update_priority':
            bug.priority = request.POST.get('priority')
            bug.save()
            messages.success(request, 'Prioridade atualizada com sucesso!')
        
        elif action == 'resolve':
            notes = request.POST.get('resolution_notes')
            bug.mark_as_resolved(notes)
            messages.success(request, 'Bug marcado como resolvido!')
        
        return redirect('store:bug_detail', bug_id=bug.id)
    
    return render(request, 'store/bug_detail.html', {'bug': bug})

@api_view(['POST'])
def report_bug(request):
    title = request.data.get('title')
    description = request.data.get('description')
    steps = request.data.get('steps')
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    
    if not all([title, description, steps, user_id, username]):
        return Response({
            'error': 'Todos os campos são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    bug = Bug.objects.create(
        title=title,
        description=description,
        steps=steps,
        user_id=user_id,
        username=username
    )
    
    return Response({
        'message': 'Bug reportado com sucesso',
        'bug_id': bug.id
    }, status=status.HTTP_201_CREATED)

def update_list(request):
    updates = Update.objects.all()
    return render(request, 'store/update_list.html', {'updates': updates})

def update_create(request):
    if request.method == 'POST':
        try:
            update = Update.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description')
            )

            # Handle multiple images
            if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    UpdateImage.objects.create(update=update, image=image)

            # Handle links
            link_titles = request.POST.getlist('link_titles[]')
            link_urls = request.POST.getlist('link_urls[]')
            for title, url in zip(link_titles, link_urls):
                if title and url:  # Only create if both fields are filled
                    UpdateLink.objects.create(update=update, title=title, url=url)

            messages.success(request, 'Atualização criada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar atualização: {str(e)}')
        
    return redirect('store:update_list')

def update_edit(request, update_id):
    update = get_object_or_404(Update, id=update_id)
    
    if request.method == 'POST':
        try:
            update.title = request.POST.get('title')
            update.description = request.POST.get('description')
            update.save()

            # Handle images
            if request.FILES.getlist('images'):
                # Remove old images if new ones are uploaded
                update.images.all().delete()
                for image in request.FILES.getlist('images'):
                    UpdateImage.objects.create(update=update, image=image)

            # Handle links
            update.links.all().delete()  # Remove old links
            link_titles = request.POST.getlist('link_titles[]')
            link_urls = request.POST.getlist('link_urls[]')
            for title, url in zip(link_titles, link_urls):
                if title and url:  # Only create if both fields are filled
                    UpdateLink.objects.create(update=update, title=title, url=url)

            messages.success(request, 'Atualização editada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao editar atualização: {str(e)}')
        return redirect('store:update_list')
    
    return render(request, 'store/update_edit.html', {'update': update})

def update_delete(request, update_id):
    if request.method == 'POST':
        update = get_object_or_404(Update, id=update_id)
        try:
            update.delete()
            messages.success(request, 'Atualização excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir atualização: {str(e)}')
    return redirect('store:update_list')

def update_image_delete(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(UpdateImage, id=image_id)
        update_id = image.update.id
        try:
            image.delete()
            messages.success(request, 'Imagem excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir imagem: {str(e)}')
        return redirect('store:update_edit', update_id=update_id)
    return redirect('store:update_list')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'store/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        try:
            event = Event.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                date=request.POST.get('date'),
                location=request.POST.get('location')
            )

            # Handle multiple images
            if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    EventImage.objects.create(event=event, image=image)

            messages.success(request, 'Evento criado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar evento: {str(e)}')
        
    return redirect('store:event_list')

def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        try:
            event.title = request.POST.get('title')
            event.description = request.POST.get('description')
            event.date = request.POST.get('date')
            event.location = request.POST.get('location')
            event.save()

            # Handle images
            if request.FILES.getlist('images'):
                # Remove old images if new ones are uploaded
                event.images.all().delete()
                for image in request.FILES.getlist('images'):
                    EventImage.objects.create(event=event, image=image)

            messages.success(request, 'Evento atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar evento: {str(e)}')
        return redirect('store:event_list')
    
    return render(request, 'store/event_edit.html', {'event': event})

def event_delete(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        try:
            event.delete()
            messages.success(request, 'Evento excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir evento: {str(e)}')
    return redirect('store:event_list')

def event_image_delete(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(EventImage, id=image_id)
        event_id = image.event.id
        try:
            image.delete()
            messages.success(request, 'Imagem excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir imagem: {str(e)}')
        return redirect('store:event_edit', event_id=event_id)
    return redirect('store:event_list')

def comingsoon_list(request):
    items = ComingSoon.objects.all()
    return render(request, 'store/comingsoon_list.html', {'items': items})

def comingsoon_create(request):
    if request.method == 'POST':
        try:
            item = ComingSoon.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                release_date=request.POST.get('release_date') or None,
                status=request.POST.get('status')
            )

            # Handle multiple images
            if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    ComingSoonImage.objects.create(coming_soon=item, image=image)

            messages.success(request, 'Item criado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar item: {str(e)}')
        
    return redirect('store:comingsoon_list')

def comingsoon_edit(request, item_id):
    item = get_object_or_404(ComingSoon, id=item_id)
    
    if request.method == 'POST':
        try:
            item.title = request.POST.get('title')
            item.description = request.POST.get('description')
            item.release_date = request.POST.get('release_date') or None
            item.status = request.POST.get('status')
            item.save()

            # Handle images
            if request.FILES.getlist('images'):
                # Remove old images if new ones are uploaded
                item.images.all().delete()
                for image in request.FILES.getlist('images'):
                    ComingSoonImage.objects.create(coming_soon=item, image=image)

            messages.success(request, 'Item atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar item: {str(e)}')
        return redirect('store:comingsoon_list')
    
    return render(request, 'store/comingsoon_edit.html', {'item': item})

def comingsoon_delete(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ComingSoon, id=item_id)
        try:
            item.delete()
            messages.success(request, 'Item excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir item: {str(e)}')
    return redirect('store:comingsoon_list')

def comingsoon_image_delete(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ComingSoonImage, id=image_id)
        item_id = image.coming_soon.id
        try:
            image.delete()
            messages.success(request, 'Imagem excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir imagem: {str(e)}')
        return redirect('store:comingsoon_edit', item_id=item_id)
    return redirect('store:comingsoon_list')

def update_list_api(request):
    updates = Update.objects.all().order_by('-created_at')
    data = []
    for update in updates:
        try:
            update_data = {
                'id': update.id,
                'title': update.title,
                'description': update.description,
                'created_at': update.created_at.isoformat() if update.created_at else None,
                'images': [],
                'links': []
            }
            
            # Handle images separately to avoid errors
            for image in update.images.all():
                try:
                    if image.image:
                        update_data['images'].append({
                            'url': request.build_absolute_uri(image.image.url)
                        })
                except:
                    continue
            
            # Handle links separately to avoid errors
            for link in update.links.all():
                try:
                    update_data['links'].append({
                        'url': link.url,
                        'title': link.title
                    })
                except:
                    continue
                    
            data.append(update_data)
        except Exception as e:
            print(f"Error processing update {update.id}: {str(e)}")
            continue
            
    return JsonResponse(data, safe=False)

def event_list_api(request):
    events = Event.objects.all().order_by('-date')
    data = []
    for event in events:
        try:
            event_data = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'date': event.date.isoformat() if event.date else None,
                'location': event.location,
                'images': []
            }
            
            # Handle images separately to avoid errors
            for image in event.images.all():
                try:
                    if image.image:
                        event_data['images'].append({
                            'url': request.build_absolute_uri(image.image.url)
                        })
                except:
                    continue
                    
            data.append(event_data)
        except Exception as e:
            print(f"Error processing event {event.id}: {str(e)}")
            continue
            
    return JsonResponse(data, safe=False)

def comingsoon_list_api(request):
    items = ComingSoon.objects.all().order_by('-release_date')
    data = []
    for item in items:
        try:
            item_data = {
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'release_date': item.release_date.isoformat() if item.release_date else None,
                'status': item.status,
                'images': []
            }
            
            # Handle images separately to avoid errors
            for image in item.images.all():
                try:
                    if image.image:
                        item_data['images'].append({
                            'url': request.build_absolute_uri(image.image.url)
                        })
                except:
                    continue
                    
            data.append(item_data)
        except Exception as e:
            print(f"Error processing coming soon item {item.id}: {str(e)}")
            continue
            
    return JsonResponse(data, safe=False) 