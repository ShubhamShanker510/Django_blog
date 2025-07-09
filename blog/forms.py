from django import forms

class BlogForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter post title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your post content here...'}), required=True)
    
    