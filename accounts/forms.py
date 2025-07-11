from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class registrationForm(forms.ModelForm):
    # Common fields
    username = forms.CharField(label="Username", min_length=5, required=True)
    email = forms.EmailField(
        label="Email",
        error_messages={"invalid": "Please enter valid EmailId"},
        required=True
    )

    # Password fields
    current_password = forms.CharField(label="Current Password", widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    confirm_new_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        is_editing = self.instance and self.instance.pk is not None

        # Only validate password change if editing and new_password was entered
        if is_editing and (new_password or confirm_new_password):
            if not current_password:
                raise forms.ValidationError("Current password is required to set a new password.")

            if not check_password(current_password, self.instance.password):
                raise forms.ValidationError("Current password is incorrect.")

            if new_password != confirm_new_password:
                raise forms.ValidationError("New password and confirmation do not match.")

        # Username uniqueness
        if username:
            qs = User.objects.filter(username=username)
            if is_editing:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Username already exists.")

        # Email uniqueness
        if email:
            qs = User.objects.filter(email=email)
            if is_editing:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Email already exists.")

        return cleaned_data
class loginForm(forms.Form):
    username=forms.CharField(label="Username", min_length=5, required=True)
    password=forms.CharField(label="Password", min_length=8, max_length=16)








































