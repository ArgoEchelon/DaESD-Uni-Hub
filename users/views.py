from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from communities.models import Community, Membership
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post
from events.models import Event

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            # Used to see errors on the form
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    
    # Get communities the user is a member of
    communities = Community.objects.filter(members=user)
    
    # Get posts authored by the user
    posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Get events organized by the user
    events = Event.objects.filter(organizer=user).order_by('start_time')[:5]
    
    # Check if the viewed profile is the current user's profile
    is_own_profile = request.user == user if request.user.is_authenticated else False
    
    context = {
        'profile_user': user,  # Using 'profile_user' to avoid conflict with 'user' template variable
        'communities': communities,
        'posts': posts,
        'events': events,
        'is_own_profile': is_own_profile
    }
    
    return render(request, 'users/user_detail.html', context)