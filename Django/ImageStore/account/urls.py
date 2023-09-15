from django.urls import re_path
from . import views

app_name = 'account'

urlpatterns = [
    re_path('login/', views.login_view, name='login'),
    re_path('register/', views.register_view, name='register'),
    re_path('logout/', views.logout_view, name='logout'),
]
