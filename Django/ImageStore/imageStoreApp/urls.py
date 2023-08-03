from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView, name='home'),
]
