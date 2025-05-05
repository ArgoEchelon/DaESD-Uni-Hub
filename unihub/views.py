from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q 
from django.contrib.auth.models import User
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

    communities = Community.objects.none()
    events = Event.objects.none()
    posts = Post.objects.none()
    users = User.objects.none()  

    if query and len(query) <= 100:  # Prevent crazy long queries slowing DB
        communities = Community.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(profile__bio__icontains=query) |
            Q(profile__major__icontains=query) |
            Q(profile__postcode__icontains=query)  
        ).distinct()

    return render(request, 'search.html', {
        'query': query,
        'communities': communities,
        'events': events,
        'posts': posts,
        'users': users,
    })