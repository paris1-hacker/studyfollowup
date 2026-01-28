from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User



class MyCustomUserCreattionForm(UserCreationForm):
    class Meta:
        model =  User
        fields = ['name', 'email', 'username', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participant']
        ordering = ['-created', '-updated']
    

class userForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'username', 'email']