from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('offersapp.urls')),
    path('tests/', include('testingasync.urls')),
]
