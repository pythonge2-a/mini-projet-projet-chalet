from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from chalet.services.sensor_service import SensorService
from chalet.services.device_service import DeviceService
import chalet.process_data.process as pd

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
    # Getting the weather data and the room data
    weather_data = SensorService.get_weather_data()
    room_data = SensorService.get_room_data()
    
    db = pd.get_db() # Do this to avoid multiple connections, here there is only one connection

    try:
        DeviceService.update_sensors(room_data, db)
    
        if request.method == 'POST':
            DeviceService.handle_lights(request, db)
        
        context = DeviceService.build_context(db, weather_data, room_data)
    finally:
        db.close_connection()
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