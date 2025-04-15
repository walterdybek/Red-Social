from django.shortcuts import render

rooms = [   # List of rooms to be displayed in the template 
    {'id':1,'name': 'Room 1', 'description': 'Description of Room 1'},
    {'id':2,'name': 'Room 2', 'description': 'Description of Room 2'},
    {'id':3,'name': 'Room 3', 'description': 'Description of Room 3'},
]


# Create your views here.
def home(request):
    context = {'rooms': rooms}  # Context dictionary to pass data to the template
    return render(request, 'base/home.html', context)  # Pass the rooms list to the template

def room(request):
    return render(request, 'room.html')

def prueba(request):
    return render(request, 'test.html')
