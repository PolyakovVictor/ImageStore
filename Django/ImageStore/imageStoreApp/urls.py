from . import views
from django.urls import include, re_path

app_name = 'imageStoreApp'

urlpatterns = [
    re_path(r'pin/(?P<id>\d+)/(?P<image_id>\d+)/$', views.pin_detail_view, name='pin_detail'),
    re_path('create_pin/', views.create_pin_view, name='create_pin'),
    re_path('user_page/', views.user_page_view, name='user_page'),
    re_path('', views.home_view, name='home'),
]
