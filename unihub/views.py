from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q 
from communities.models import Community
from events.models import Event
from posts.models import Post

def home(request):
    communities = Community.objects.all()[:5]
    events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:5]
    return render(request, 'home.html', {
        'communities': communities,
        'events': events
    })

def search(request):
    query = request.GET.get('q', '').strip() 
    
    if query:
        communities = Community.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)   
        ).distinct()

        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) 
        )

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) 
        )
    else:
        communities = Community.objects.none()
        events = Event.objects.none()
        posts = Post.objects.none()
    
    return render(request, 'search.html', {
        'communities': communities,
        'events': events,
        'posts': posts,
        'query': query
    })
