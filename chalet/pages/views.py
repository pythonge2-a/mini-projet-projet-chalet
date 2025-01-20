from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from chalet.mqtt_client import publish_message, get_value
from meteo.__meteo__ import load_history, get_weather_data

import io

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@login_required
def graphics_view(request):
    context = {'timestamp' : timezone.now().timestamp()}
    return render(request, 'graphics.html')

@login_required
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
        history = load_history()
        temperature_value, pressure_value, humidity_value, weather_description = get_weather_data(history, save=False)
        if temperature_value is None or humidity_value is None or pressure_value is None or weather_description is None:
            raise Exception('Error while getting weather data')
        room_temp = get_value("capteur/temperature")
        room_humidity = get_value("capteur/humidite")
        if room_temp is None or room_humidity is None:
            raise Exception('Error while getting room data')
    except Exception as e:
        print(f"Error: {e}")
        temperature_value = 'Erreur de récupération des données'
        pressure_value = 'Erreur de récupération des données'
        humidity_value = 'Erreur de récupération des données'
        weather_description = 'Erreur de récupération des données'
        room_temp = 'Erreur de récupération des données'
        room_humidity = 'Erreur de récupération des données'
    
    if request.method == 'POST':
        print("POST request received", request.POST)
        light_status_room = request.POST.get('toggle_light_room') == 'on'
        light_status_living = request.POST.get('toggle_light_living') == 'on'
        light_status_kitchen = request.POST.get('toggle_light_kitchen') == 'on'
        light_status_bathroom = request.POST.get('toggle_light_bathroom') == 'on'

        if 'toggle_light_room' in request.POST:
            print(f"Light status room: {light_status_room}")
            publish_message('intLed/ON' if light_status_room else 'intLed/OFF')

    
    context = {
        'room_temperature_value': room_temp,
        'room_humidity_value': room_humidity,
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
        # Données météo extérieure
        'outside_temperature_value': temperature_value,
        'outside_pressure_value': pressure_value,
        'outside_humidity_value': humidity_value,
        'outside_weather' : weather_description,
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