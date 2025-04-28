from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Post, Comment
from .forms import PostForm, CommentForm
from communities.models import Community, Membership
def post_list(request):
    filter_option = request.GET.get('filter', None)
    search_query = request.GET.get('q', '')  # New: get search query

    if filter_option == 'my_posts' and request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
    elif request.user.is_authenticated:
        user_communities = request.user.communities.all()
        posts = Post.objects.filter(community__in=user_communities).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    # New: Apply search filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(community__name__icontains=search_query)
        )

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'filter': filter_option,
        'search_query': search_query
    })
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
    
    # Toggle like status
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, 'You unliked this post.')
    else:
        post.likes.add(request.user)
        messages.success(request, 'You liked this post.')
    
    # Get the referer URL to redirect back to the same page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('post_detail', pk=post.pk)
    
def popular_posts(request):
    posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    return render(request, 'posts/popular_posts_snippet.html', {'posts': posts})