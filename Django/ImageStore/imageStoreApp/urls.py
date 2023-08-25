from . import views
from django.urls import include, path

app_name = 'imageStoreApp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pin/<int:id>', views.pin_detail, name='pin_detail'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.register, name='registration'),
    path('logout/', views.logout_view, name='logout')
]
