from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError(
                "El nombre de usuario no está disponible"
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError(
                "El correo electrónico ya está en uso"
            )
        return email

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return data

    def save(self):
        data = self.cleaned_data
        data.pop("password_confirmation")
        return User.objects.create_user(**data)