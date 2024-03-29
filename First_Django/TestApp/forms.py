from django.db.models import fields
from django.forms import ModelForm, models
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['host','participants']