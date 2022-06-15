from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import *


def menu(request):
    code = request.GET.get('desk', None)
    if not code:
        raise Http404
    
    desk = get_object_or_404(Desk, code=code)
    categories = Category.objects.all()
    
    return render(request, 'menu.html', {'desk': desk,
                                         'categories': categories})
    
    
def request_waiter(request):
    code = request.GET.get('desk', None)
    if not code:
        raise Http404
    
    desk = get_object_or_404(Desk, code=code)
    
    request = Requests(desk=desk)
    request.save()
    return JsonResponse({'success': True})

@login_required()
def waiter(request):
    return render(request, 'waiter.html')