from django.shortcuts import render, redirect
from django.http import HttpResponse  # Import HttpResponse for returning HTTP responses
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm for user registration
from .models import Room, Topic, Message # Import Room, Topic, Message, and Profile models
from .forms import RoomForm, UserForm  # Import RoomForm and UserForm for creating and updating rooms and users
from .forms import CustomUserCreationForm



# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'base/login.html', {'form': form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__contains=q)) # Fetch all Room objects from the database
    topics = Topic.objects.all()[0:5]  # Fetch all Topic objects from the database
    room_count = rooms.count()  # Count the number of rooms
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) | Q(room__name__icontains=q) | Q(room__description__contains=q))  # Fetch all messages related to the rooms
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}  # Context dictionary to pass data to the template
    return render(request, 'base/home.html', context)  # Pass the rooms list to the template

def room(request,pk):
    room = Room.objects.get(id=pk)  # Fetch a specific Room object by its primary key (pk)
    room_message = room.message_set.all().order_by('-created')  # Fetch all messages related to the room and order them by creation date
    participants = room.participants.all()  # Fetch all participants in the room
    if request.method == 'POST':
        message= Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))  # Create a new message object 
        room.participants.add(request.user)  # Add the user to the room's participants
        return redirect('room', pk=room.id)  # Redirect to the same room page after posting a message
    context = {'room': room, 'room_message': room_message,'participants':participants }  # Context dictionary to pass data to the template
    return render(request, 'base/room.html',context)

def prueba(request):
    return render(request, 'test.html')


def userProfile(request,pk):
    user = User.objects.get(id=pk)  # Fetch a specific User object by its primary key (pk)
    rooms = user.room_set.all()  # Fetch all rooms created by the user
    room_messages = user.message_set.all()  # Fetch all messages sent by the user
    topics = Topic.objects.all()  # Fetch all Topic objects from the database
    context = {'user': user, 'rooms': rooms,'room_messages': room_messages, 'topics': topics }  # Context dictionary to pass data to the template
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')  # Require login to access this view
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()  # Save the room to the database    
            return redirect('home')
    context = {'form': form}  # Context dictionary to pass data to the template
    return render(request, 'base/room_form.html',context)


@login_required(login_url='login')  # Require login to access this view
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:  # Check if the user is not the host of the room
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}  # Context dictionary to pass data to the template
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')  # Require login to access this view
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:  # Check if the user is not the host of the room
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}  # Context dictionary to pass data to the template
    return render(request, 'base/delete.html', {'obj':room})  # Pass the room object to the template

@login_required(login_url='login') 
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:  # Check if the user is not the host of the room
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)  # Redirect to the room page after deleting the message
    context = {'obj': message}  # Context dictionary to pass data to the template
    return render(request, 'base/delete.html', {'obj':message})  # Pass the room object to the template


@login_required(login_url='login') 
def updateUser(request):
    user= request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})  # Pass the form to

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)  # Fetch all Topic objects from the database
    context = {'topics': topics}  # Context dictionary to pass data to the template
    return render(request, 'base/topics.html', context)  # Pass the rooms list to the template

def activityPage(request):
    room_messages = Message.objects.all()  # Fetch all messages related to the rooms
    context = {'room_messages': room_messages}  # Context dictionary to pass data to the template
    return render(request, 'base/activity.html', context)  # Pass the rooms list to the template


#login resgirtro 
