from django import forms
from django.contrib.auth.models import User


class registrationForm(forms.ModelForm):
    username=forms.CharField(label="Username", min_length=5, required=True)
    email=forms.EmailField(label="Email", error_messages={"invalid":"Please enter valid EmailId"}, required=True)
    password=forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8, max_length=16, required=False)
    confirmPassword=forms.CharField(label="Confirm Password", widget=forms.PasswordInput, min_length=8, max_length=16, required=False)

    class Meta:
        model=User
        fields=['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirmPassword')

        is_editing = self.instance and self.instance.pk is not None
        if not is_editing and not password:
            raise forms.ValidationError("Password is required for new user.")


        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("password and confirm password does not match")
        
        if username:
            qs = User.objects.filter(username=username)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Username already exists")

    # ✅ Unique email (optional: also exclude self)
        if email:
            qs = User.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Email already exists")

        return cleaned_data

class loginForm(forms.Form):
    username=forms.CharField(label="Username", min_length=5, required=True)
    password=forms.CharField(label="Password", min_length=8, max_length=16)








































