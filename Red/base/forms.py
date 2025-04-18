from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # This will include all fields in the Room model
        exclude = ['host','participants']  # Exclude the 'id' field if you want to auto-generate it


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include the fields you want to allow the user to update