from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
import io

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@login_required
def graphics_view(request):
    context = {'timestamp' : timezone.now().timestamp()}
    return render(request, 'graphics.html')

def graph_view(request):
    with open('meteo/graphs/simple_graph.png', 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

light_status_room = False
light_status_living = False
light_status_kitchen = False
light_status_bathroom = False
@login_required
def captors_view(request):
    global light_status_room, light_status_living, light_status_kitchen, light_status_bathroom
    try:
        temperature_value = 22.5  # Remplacez par la méthode réelle pour obtenir la valeur du capteur
        humidity_value = 50.0  # Remplacez par la méthode réelle pour obtenir la valeur du capteur
        co2_value = 400  # Remplacez par la méthode réelle pour obtenir la valeur du capteur
    except Exception as e:
        print(f"Error: {e}")
        temperature_value = 'Erreur de récupération des données'
        humidity_value = 'Erreur de récupération des données'
        co2_value = 'Erreur de récupération des données'
    
    if request.method == 'POST':
        light_status_room = 'toggle_light_room' in request.POST
        light_status_living = 'toggle_light_living' in request.POST
        light_status_kitchen = 'toggle_light_kitchen' in request.POST
        light_status_bathroom = 'toggle_light_bathroom' in request.POST
    
    context = {
        'room_temperature_value': 22.5,
        'room_humidity_value': 50.0,
        'light_status_room' : light_status_room,
        'living_temperature_value': 22.5,
        'living_humidity_value': 50.0,
        'light_status_living' : light_status_living,
        'kitchen_temperature_value': 22.5,
        'kitchen_humidity_value': 50.0,
        'light_status_kitchen' : light_status_kitchen,
        'bathroom_temperature_value': 22.5,
        'bathroom_humidity_value': 50.0,
        'light_status_bathroom' : light_status_bathroom,
        'outside_temperature_value': 15,
        'outside_humidity_value': 60.0,
    }
    return render(request, 'captors.html', context)

def register(request: Any) -> Any:
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {
        'form': form,
        'title': 'Register'
    })