from django import forms
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Finance', 'Finance'),
    ]



class BlogForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter post title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your post content here...'}), required=True)
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.Select()
    )

class BlogForm1(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter post title'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your post content here...'}),
        required=True
    )

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.Select()
    )

    author = forms.ModelChoiceField(
        queryset=User.objects.filter(),
        required=True,
        empty_label="Select Author"
    )