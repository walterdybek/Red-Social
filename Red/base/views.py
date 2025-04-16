from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm




# Create your views here.
def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)  # Fetch all Room objects from the database
    topics = Topic.objects.all()  # Fetch all Topic objects from the database
    context = {'rooms': rooms, 'topics':topics}  # Context dictionary to pass data to the template
    return render(request, 'base/home.html', context)  # Pass the rooms list to the template

def room(request,pk):
    room = Room.objects.get(id=pk)  # Fetch a specific Room object by its primary key (pk)
    return render(request, 'base/room.html')

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


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}  # Context dictionary to pass data to the template
    return render(request, 'base/delete.html', {'obj':room})  # Pass the room object to the template
