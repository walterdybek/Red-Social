from django.shortcuts import render, redirect
from django.http import HttpResponse  # Import HttpResponse for returning HTTP responses
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm for user registration
from .models import Room, Topic, Message
from .forms import RoomForm




# Create your views here.

def loginPage(request):
    page = 'login'  # Set the page variable to 'login'
    if request.user.is_authenticated:  # Check if the user is already authenticated
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()  # Get the username from the POST request and convert it to lowercase
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page':page}  # Context dictionary to pass data to the template
    return render(request, 'base/login_registration.html', context)  # Pass the page variable to the template


def logoutUser(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page

def registerPage(request):
    form = UserCreationForm()  # Create an instance of UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # Convert username to lowercase
            user.save()  # Save the user to the database
            login(request, user)
            return redirect('home')  # Redirect to the login page
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_registration.html',{'form':form})  # Pass the page variable to the template

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__contains=q)) # Fetch all Room objects from the database
    topics = Topic.objects.all()  # Fetch all Topic objects from the database
    room_count = rooms.count()  # Count the number of rooms
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count}  # Context dictionary to pass data to the template
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

@login_required(login_url='login')  # Require login to access this view
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
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
        return redirect('home')
    context = {'obj': room}  # Context dictionary to pass data to the template
    return render(request, 'base/delete.html', {'obj':message})  # Pass the room object to the template