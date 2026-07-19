from django.contrib import admin
from django.urls import path

admin.autodiscover()

urlpatterns = [
    path('foo/bar/', admin.site.urls),
]
