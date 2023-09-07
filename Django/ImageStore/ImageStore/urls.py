from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('account/', include('account.urls')),
    re_path('', include('imageStoreApp.urls')),
]
