from django.contrib import admin
from django.urls import path, include  # include is necessary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),  # Include the chat app URLs
    
]
