from . import views
from django.urls import re_path

app_name = 'imageStoreApp'

urlpatterns = [
    re_path(r'pin/(?P<id>\d+)/(?P<image_id>\d+)/$', views.pin_detail_view, name='pin_detail'),
    re_path('create_pin/', views.create_pin_view, name='create_pin'),
    re_path('user_page/', views.user_page_view, name='user_page'),
    re_path('create_board/', views.create_board_view, name='create_board'),
    re_path(r'board/(?P<board_id>\d+)/$', views.board_detail_view, name='board_detail'),
    re_path(r'add_pin_to_favorite/(?P<pin_id>\d+)/(?P<image_id>\d+)/$', views.add_pin_to_favorite, name='add_pin_to_favorite'),
    re_path('favorite/', views.favorite_view, name='favorite'),
    re_path('', views.home_view, name='home'),
]
