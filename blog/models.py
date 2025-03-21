from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="A brief description that appears on the home page", blank=True, null=True)
    content = models.TextField(help_text="The full content of your blog post")
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
