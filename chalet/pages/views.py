from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from typing import Any

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@login_required
def graph_view(request):
    return render(request, 'graphics.html')

light_status = False
@login_required
def captors_view(request):
    global light_status
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
        light_status = 'toggle_light' in request.POST
    
    context = {
        'temperature_value': temperature_value,
        'humidity_value': humidity_value,
        'co2_value': co2_value,
        'light_status': light_status,
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