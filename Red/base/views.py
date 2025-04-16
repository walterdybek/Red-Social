from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm




# Create your views here.
def home(request):
    rooms = Room.objects.all()  # Fetch all Room objects from the database
    context = {'rooms': rooms}  # Context dictionary to pass data to the template
    return render(request, 'base/home.html', context)  # Pass the rooms list to the template

def room(request,pk):
    room = Room.objects.get(id=pk)  # Fetch a specific Room object by its primary key (pk)
    return render(request, 'room.html')

def prueba(request):
    return render(request, 'test.html')

def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}  # Context dictionary to pass data to the template
    return render(request, 'base/room_form.html',context)



def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}  # Context dictionary to pass data to the template
    return render(request, 'base/room_form.html',context)

