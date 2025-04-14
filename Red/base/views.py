from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html', {'resultado': 2 + 2})

def room(request):
    return render(request, 'room.html')

def prueba(request):
    return render(request, 'test.html')
