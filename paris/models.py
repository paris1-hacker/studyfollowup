from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


# a room is a child of a topic - 
class Topic(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Room (models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # a topic can have multiple room, whereas a room can hve one topic 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    participant = models.ManyToManyField(User, related_name='participant', blank=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        ordering = ['-created', '-updated']
    
# each room should have a user 
class Message(models.Model):
    # the values for the message
    # a user can have many messeages, wheerease a message can how only one user.  
    user = models.ForeignKey(User, on_delete=models.CASCADE  )
    # specify the room 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = [
            '-created', '-updated'
        ]

    def __str__(self):
        return self.body[0:50]
    
