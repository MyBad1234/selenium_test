from django.contrib import admin
from django.urls import path

from selenium_client.views import search_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_view)
]
