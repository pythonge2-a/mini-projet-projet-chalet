from django.urls import path
from .views import home_view, graph_view

urlpatterns = [
    path('', home_view, name='home'),
    path('graphics/', graph_view, name='graphics'),
]
