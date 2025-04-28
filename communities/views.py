from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Community, Membership
from . forms import CommunityForm
from django.db.models import Q

@login_required
def community_list(request):
    query = request.GET.get('q', '')
    communities = Community.objects.all()

    if query:
        keywords = [kw.strip() for kw in query.split(',') if kw.strip()]
        q_objects = Q()

        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword) | Q(tags__name__icontains=keyword)

        communities = communities.filter(q_objects).distinct()

    return render(request, 'communities/communities.html', {'communities': communities, 'query': query})

@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    is_member = request.user.communities.filter(id=community.id).exists()
    return render(request, 'communities/community_detail.html', {
        'community': community,
        'is_member': is_member
    })

@login_required
def community_create(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = request.user
            community.save()
            Membership.objects.create(user=request.user, community=community, role='ADMIN')
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm()
    return render(request, 'communities/community_form.html', {'form': form})

@login_required
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if not request.user.communities.filter(id=community.id).exists():
        Membership.objects.create(user=request.user, community=community, role='MEMBER')
    return redirect('community_detail', pk=community.pk)

@login_required
def community_delete(request, pk):
    community = get_object_or_404(Community, pk=pk)
    
    # Check if user is the owner or has admin rights
    if request.user != community.owner:
        membership = get_object_or_404(Membership, user=request.user, community=community)
        if membership.role != 'ADMIN':
            messages.error(request, 'You must be the community owner to delete it.')
            return redirect('community_detail', pk=community.pk)
    
    if request.method == 'POST':
        community_name = community.name
        community.delete()
        messages.success(request, f'Community "{community_name}" has been deleted.')
        return redirect('community_list')
    
    return render(request, 'communities/community_confirm_delete.html', {'community': community})

@login_required
def community_edit(request, pk):
    community = get_object_or_404(Community, pk=pk)
    
    # Check if user is the owner or has admin rights
    if request.user != community.owner:
        membership = get_object_or_404(Membership, user=request.user, community=community)
        if membership.role != 'ADMIN':
            messages.error(request, 'You must be the community owner to edit it.')
            return redirect('community_detail', pk=community.pk)
    
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, f'Community "{community.name}" has been updated!')
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm(instance=community)
    
    return render(request, 'communities/community_form.html', {
        'form': form,
        'edit_mode': True,
        'community': community
    })