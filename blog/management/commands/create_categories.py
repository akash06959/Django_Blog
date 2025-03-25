from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for the blog'

    def handle(self, *args, **kwargs):
        categories = [
            'Technology',
            'Travel',
            'Food',
            'Lifestyle',
            'Health & Fitness',
            'Business',
            'Education',
            'Entertainment',
            'Science',
            'Sports'
        ]

        for category_name in categories:
            Category.objects.get_or_create(
                name=category_name,
                slug=slugify(category_name)
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_name}"')
            ) 