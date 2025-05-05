from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Post, Comment
from .forms import PostForm, CommentForm
from communities.models import Community, Membership, Tag

def post_list(request):
    query = request.GET.get('q', '')
    filter_option = request.GET.get('filter', None)
    search_query = request.GET.get('q', '')  # Get search query
    
    posts = Post.objects.all()

    if filter_option == 'my_posts' and request.user.is_authenticated:
        posts = posts.filter(author=request.user)
    elif request.user.is_authenticated:
        user_communities = request.user.communities.all()
        posts = posts.filter(community__in=user_communities)
    
    if query:
        keywords = [kw.strip() for kw in query.split(',') if kw.strip()]
        q_objects = Q()

        for keyword in keywords:
            q_objects |= Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(tags__name__icontains=keyword)

        posts = posts.filter(q_objects).distinct()

    posts = posts.order_by('-created_at')

    return render(request, 'posts/post_list.html', {'posts': posts, 'filter': filter_option, 'query': query})

    # Apply search filter
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

            tag_string = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)

            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form, 'community': community})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tags.clear()

            tag_string = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)

            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', pk=post.pk)
    else:
        initial_tags = ', '.join(tag.name for tag in post.tags.all())
        form = PostForm(instance=post, initial={'tags': initial_tags})

    return render(request, 'posts/post_form.html', {
        'form': form,
        'community': post.community,
        'edit_mode': True,
        'post': post
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
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