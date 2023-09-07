from . import views
from django.urls import include, re_path

app_name = 'imageStoreApp'

urlpatterns = [
    re_path(r'^pin/(?P<id>[a-zA-Z0-9-]+)/$', views.pin_detail, name='pin_detail'),
    re_path('', views.home_view, name='home'),
]
