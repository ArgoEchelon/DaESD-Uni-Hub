from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Participation
from .forms import EventForm
from communities.models import Community

@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_participant = request.user.events.filter(id=event.id).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_participant': is_participant
    })

@login_required
def event_create(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.community = community
            event.save()
            Participation.objects.create(user=request.user, event=event, status='GOING')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'community': community})

@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.events.filter(id=event.id).exists():
        Participation.objects.create(user=request.user, event=event, status='GOING')
    return redirect('event_detail', pk=event.pk)