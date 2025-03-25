from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    spam_words = models.TextField(blank=True, help_text="Enter spam words separated by commas")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_spam_words_list(self):
        """Convert spam words string to a list of words"""
        if not self.spam_words:
            return []
        return [word.strip().lower() for word in self.spam_words.split(',')]

    def check_spam(self, text):
        """Check if text contains any spam words"""
        if not self.spam_words:
            return False, text
        
        spam_words = self.get_spam_words_list()
        text_lower = text.lower()
        
        for word in spam_words:
            if word in text_lower:
                # Replace spam word with asterisks
                censored_text = text
                while word in text_lower:
                    start = text_lower.find(word)
                    end = start + len(word)
                    censored_text = censored_text[:start] + '*' * len(word) + censored_text[end:]
                    text_lower = censored_text.lower()
                return True, censored_text
        
        return False, text

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="A brief description that appears on the home page", blank=True, null=True)
    content = models.TextField(help_text="The full content of your blog post")
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} {self.notification_type}d on {self.post.title}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
