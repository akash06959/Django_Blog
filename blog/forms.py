from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'website', 'spam_words']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'spam_words': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter spam words separated by commas (e.g., spam, bad, inappropriate)'
            })
        }

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter title'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3',
        'placeholder': 'Enter a brief description'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '10',
        'placeholder': 'Write your post content here'
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=False,
        empty_label="Select a category"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        } 