from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Community, Membership
from . forms import CommunityForm

@login_required
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'communities/community_list.html', {'communities': communities})

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
