from django import forms
from .models import Post, Comment, Rating

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'url', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

