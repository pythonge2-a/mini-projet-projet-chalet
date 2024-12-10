from django.urls import path
from .views import home_view, graph_view, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main pages
    path('', home_view, name='home'),
    path('graphics/', graph_view, name='graphics'),
    
    # Authentication paths
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
]
