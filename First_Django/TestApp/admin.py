from django.contrib import admin
from django.db.models.base import Model
from .models import Message, Room, Topic

# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)