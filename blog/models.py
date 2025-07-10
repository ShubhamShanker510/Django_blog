from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Finance', 'Finance'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Technology')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  