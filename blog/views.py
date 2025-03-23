from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment, UserProfile, Notification
from .forms import UserRegistrationForm, UserProfileForm, PostForm, CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all().select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_liked = request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()
    recent_posts = Post.objects.exclude(id=post_id).order_by('-published_date')[:3]
    comments = post.comments.all().select_related('author')
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'user_liked': user_liked,
        'recent_posts': recent_posts,
        'comments': comments,
        'comment_form': comment_form
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    liked_posts = Post.objects.filter(likes=request.user).order_by('-published_date')
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]
    unread_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    context = {
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'blog/dashboard.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'blog/profile_edit.html', {'form': profile_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        messages.error(request, "You cannot like your own post.")
        return redirect('post_detail', post_id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.info(request, "You unliked this post.")
    else:
        post.likes.add(request.user)
        messages.success(request, "You liked this post!")
        # Create notification for post author
        Notification.objects.create(
            recipient=post.author,
            notification_type='like',
            post=post,
            sender=request.user,
            message=f"{request.user.username} liked your post '{post.title}'"
        )
    
    return redirect('post_detail', post_id=post_id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Check for spam words
            is_spam, censored_content = post.author.userprofile.check_spam(comment.content)
            comment.content = censored_content
            comment.save()
            
            # Create notification for spam detection
            if is_spam:
                Notification.objects.create(
                    recipient=post.author,
                    notification_type='spam',
                    post=post,
                    sender=request.user,
                    message=f"Spam word detected and censored in a comment on your post '{post.title}' by {request.user.username}"
                )
                messages.warning(request, 'Your comment contained inappropriate words and was censored.')
            else:
                messages.success(request, 'Your comment has been added successfully!')
            
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'comments': post.comments.all().order_by('-created_date')
    })
