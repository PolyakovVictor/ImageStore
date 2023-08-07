from . import views
from django.urls import include, path

app_name = 'imageStoreApp'

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('users/', include('django.contrib.auth.urls'))
]
