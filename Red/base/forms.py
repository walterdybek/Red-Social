from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # This will include all fields in the Room model
        exclude = ['host','participants']  # Exclude the 'id' field if you want to auto-generate it