from django.forms import ModelForm
from .models import Room , Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # This will include all fields in the Room model
        exclude = ['host','participants']  # Exclude the 'id' field if you want to auto-generate it


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include the fields you want to allow the user to update

#usuario form
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    last_name = forms.CharField(
        label="Apellidos", 
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    email = forms.EmailField(
        label="Correo UFV",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    birthdate = forms.DateField(
        label="Fecha de nacimiento",
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthdate', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@ufv.es'):
            raise ValidationError("Por favor usa tu correo institucional @ufv.es")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.ufv_email = self.cleaned_data['email']
            profile.birthdate = self.cleaned_data['birthdate']
            profile.save()
        return user