from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from chalet.mqtt_client import publish_message, get_value
from chalet.meteo.meteo import load_history, get_weather_data
import chalet.process_data as pd
import chalet.database as db

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

@login_required
def captors_view(request):
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
        temperature_value = 'N/A'
        pressure_value = 'N/A'
        humidity_value = 'N/A'
        weather_description = 'N/A'
        room_temp = 'N/A'
        room_humidity = 'N/A'

    db.update_device_state("temperature sensor_bedroom", str(room_temp) + "°C")
    db.update_device_state("humidity sensor_all", str(room_humidity) + "%")
    
    if request.method == 'POST':
        print("POST request received", request.POST)
        db.update_device_state("lamp_bedroom_switch", "on" if request.POST.get('toggle_light_room') == 'on' else "off")
        db.update_device_state("lamp_living_room_switch", "on" if request.POST.get('toggle_light_living') == 'on' else "off")
        db.update_device_state("lamp_kitchen_switch", "on" if request.POST.get('toggle_light_kitchen') == 'on' else "off")
        db.update_device_state("lamp_bathroom_switch", "on" if request.POST.get('toggle_light_bathroom') == 'on' else "off")

        if 'toggle_light_room' in request.POST:
            print(f"Light status room: {db.get_device_state('lamp_bedroom')}")
            publish_message('intLed/ON' if db.get_device_state('lamp_bedroom') == 1 else 'intLed/OFF')

    
    context = {
        'room_temperature_value': db.get_device_state('temperature sensor_bedroom'),
        'room_humidity_value': db.get_device_state('humidity sensor_all'),
        'light_status_room' : db.get_device_state('lamp_bedroom_switch') == 1,
        'living_temperature_value': 22.5,
        'living_humidity_value': 50.0,
        'light_status_living' : db.get_device_state('lamp_living_room_switch') == 1,
        'kitchen_temperature_value': 22.5,
        'kitchen_humidity_value': 50.0,
        'light_status_kitchen' : db.get_device_state('lamp_kitchen_switch') == 1,
        'bathroom_temperature_value': 22.5,
        'bathroom_humidity_value': 50.0,
        'light_status_bathroom' : db.get_device_state('lamp_bathroom_switch') == 1,
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