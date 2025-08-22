from .models import Posts, Comment
from django import forms
from django.views.generic import ListView, DetailView

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('username', 'comment_text')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'comment_text': forms.Textarea(attrs={'class': 'form-control'})
        }

class SearchForm(forms.Form):
    Q = forms.IntegerField(label='Search')