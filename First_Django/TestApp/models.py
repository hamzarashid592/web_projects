from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Topic(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL ,null=True)
    host=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated_on','-created_on']


    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField(null=False)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]