from . import views
from django.urls import include, path

app_name = 'imageStoreApp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pin/<int:id>', views.pin_detail, name='pin_detail'),
    path('users/', include('django.contrib.auth.urls'))
]
