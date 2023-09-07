from django.urls import re_path
from . import views

app_name = 'account'

urlpatterns = [
    re_path('login/', views.login_view, name='login'),
    re_path('register/', views.register_view, name='register'),
    re_path('login_api/', views.login_api, name='login_api'),
    re_path('register_api/', views.register_api, name='register_api'),
    re_path('test_token/', views.test_token),
    re_path('logout/', views.logout_view, name='logout'),
]
