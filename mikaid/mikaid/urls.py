
from django.contrib import admin
from django.urls import path, include # This needs to be added

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('api.urls')),
]
