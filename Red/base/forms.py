from django.forms import ModelForm
from .models import Room
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
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthdate', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user