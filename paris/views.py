from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm
from django.db.models.aggregates import Count
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Message
from .forms import userForm, MyCustomUserCreattionForm


def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else '' 
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)|
        Q(host__username__icontains=q)
    )
    room = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains =q)
    )

    context = {'rooms': rooms, 'rount_count': room, 'topics': topics, 'room_messages': room_messages}

    return render(request, 'paris/home.html', context)


def room(request, pk):
    room =  get_object_or_404(Room, pk=pk)
    room_messages= room.message_set.all()  
    participant = room.participant.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participant.add(request.user)  #to make sure a user that commented will be added to the room
        return redirect('room', pk=room.id, )
    context = {'room': room, 'room_messages': room_messages, 'participant': participant}
    return render(request, 'paris/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
       topic_name = request.POST.get('topic')
       (topic, created) = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host = request.user,
           topic= topic, 
           name = request.POST.get('name')
       )
       return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
            
    context = {'form': form, 'topics':topics}
    return render(request, 'paris/roomform.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form =  RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room ')
    

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')
    #     form = RoomForm(request.POST, instance=room)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
        

    context = {'form': form, 'room':room, 'topics':topics}
    return render(request, 'paris/roomform.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room ')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'paris/delete.html', {'obj': room})


def loginPage(request):
    page = 'login' 
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'No user Exist with that username')

        user = authenticate(request, email=email, password=password)

        if user != None:
            login(request, user)
            return redirect('home')

    return render(request, 'paris/login_register.html', {'page': page})



def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyCustomUserCreattionForm

    if request.method == 'POST':
        form = MyCustomUserCreattionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'An error Occuped')
    return render(request, 'paris/login_register.html', {'form': form})



def deleteMessage(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.user != message.user:
        return HttpResponse('You cant delete this message ')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'paris/delete.html', context)


def deleteActivity(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this room')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'paris/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user':user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'paris/profile.html', context)


def editProfile(request):
    user = request.user
    form = userForm(instance=user)

    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'paris/edit-user.html', context)


def moreSection(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics =  Topic.objects.filter(
        name__icontains=q
    )
    context = {'topics': topics}
    return render(request, 'paris/topics.html', context)