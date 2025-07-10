from django import forms
from django.contrib.auth.models import User
from .models import Category

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
    category = forms.ModelChoiceField(
    queryset=Category.objects.all(),
    required=True,
    empty_label="Select Category"
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

    category = forms.ModelChoiceField(
    queryset=Category.objects.all(),
    required=True,
    empty_label="Select Category"
    )

    author = forms.ModelChoiceField(
        queryset=User.objects.filter(),
        required=True,
        empty_label="Select Author"
    )

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name