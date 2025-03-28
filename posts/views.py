from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from communities.models import Community, Membership

def post_list(request, community_pk=None):
    # If a community ID is provided, filter posts by that community
    if community_pk:
        community = get_object_or_404(Community, pk=community_pk)
        posts = Post.objects.filter(community=community).order_by('-created_at')
        context = {'posts': posts, 'community': community}
    else:
        # If no community ID is provided, show all posts or posts from user's communities
        if request.user.is_authenticated:
            # Note: Undecided which method preferred
            # Option 1: Show posts from communities the user is a member of
            user_communities = request.user.communities.all()
            posts = Post.objects.filter(community__in=user_communities).order_by('-created_at')
            # Option 2: Show all posts 
            # posts = Post.objects.all().order_by('-created_at')
        else:
            # For non-authenticated users, show all posts
            posts = Post.objects.all().order_by('-created_at')
        context = {'posts': posts}
    
    return render(request, 'posts/post_list.html', context)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_create(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Check if user is a member of the community
    if not Membership.objects.filter(user=request.user, community=community).exists():
        messages.error(request, 'You must be a member of the community to create posts.')
        return redirect('community_detail', pk=community.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'posts/post_form.html', {'form': form, 'community': community})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {
        'form': form, 
        'community': post.community,
        'edit_mode': True,
        'post': post
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        community_pk = post.community.pk
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('community_detail', pk=community_pk)
    
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=post.pk)