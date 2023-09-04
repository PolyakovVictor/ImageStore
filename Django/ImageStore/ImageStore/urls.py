from django.contrib import admin
from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    # re_path('', include('imageStoreApp.urls'))
    re_path('login/', views.login_view, name='login'),
    re_path('register/', views.register_view, name='register'),
    re_path('test_token/', views.test_token),
]
