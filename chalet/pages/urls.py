from django.urls import path
from .views import home_view, graph_view, captors_view, register
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main pages
    path('', home_view, name='home'),
    path('graphics/', graph_view, name='graphics'),
    path('captors/', captors_view, name='captors'),
    
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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)