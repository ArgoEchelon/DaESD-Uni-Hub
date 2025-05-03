from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, Participation
from .forms import EventForm
from communities.models import Community, Membership, Tag

def event_list(request):
    filter_option = request.GET.get('filter', None)
    
    if filter_option == 'attending' and request.user.is_authenticated:
        # Get events the user is attending
        events = Event.objects.filter(participants=request.user).order_by('start_time')
    else:
        # Show all upcoming events
        events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    
    return render(request, 'events/event_list.html', {'events': events, 'filter': filter_option})

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

            tag_string = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                event.tags.add(tag)

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

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.organizer:
        messages.error(request, 'You can only edit events you organized.')
        return redirect('event_detail', pk=event.pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            event.tags.clear()

            tag_string = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                event.tags.add(tag)

            messages.success(request, 'Event has been updated!')
            return redirect('event_detail', pk=event.pk)
    else:
        initial_tags = ', '.join(tag.name for tag in event.tags.all())
        form = EventForm(instance=event, initial={'tags': initial_tags})

    return render(request, 'events/event_form.html', {
        'form': form,
        'community': event.community,
        'edit_mode': True,
        'event': event
    })

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user is the organizer
    if request.user != event.organizer:
        messages.error(request, 'You can only delete events you organized.')
        return redirect('event_detail', pk=event.pk)
    
    if request.method == 'POST':
        community_pk = event.community.pk
        event.delete()
        messages.success(request, 'Event has been deleted!')
        return redirect('community_detail', pk=community_pk)
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})