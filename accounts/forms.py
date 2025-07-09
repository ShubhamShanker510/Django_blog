from django import forms
from django.contrib.auth.models import User


class registrationForm(forms.ModelForm):
    username=forms.CharField(label="Username", min_length=5, required=True)
    email=forms.EmailField(label="Email", error_messages={"invalid":"Please enter valid EmailId"}, required=True)
    password=forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8, max_length=16, required=True)
    confirmPassword=forms.CharField(label="Confirm Password", widget=forms.PasswordInput, min_length=8, max_length=16, required=True)

    class Meta:
        model=User
        fields=['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirmPassword')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("password and confirm password does not match")
        
        if email and '@' not in email:
            raise forms.ValidationError("Invalid Email, Please enter again")

class loginForm(forms.Form):
    username=forms.CharField(label="Username", min_length=5, required=True)
    password=forms.CharField(label="Password", min_length=8, max_length=16)


# class Reset_Password(forms.Form):
#     username=forms.CharField(label="Username", min_length=5, required=True)
#     password=forms.CharField(label="Password", min_length=8, max_length=16)









































