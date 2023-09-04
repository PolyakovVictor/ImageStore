from . import views
from django.urls import include, re_path

app_name = 'imageStoreApp'

urlpatterns = [
    re_path('', views.home_view, name='home'),
    re_path('pin/<int:id>', views.pin_detail, name='pin_detail'),
    re_path('login/', views.login_view, name='login'),
    re_path('registration/', views.register, name='registration'),
    re_path('logout/', views.logout_view, name='logout')
]
