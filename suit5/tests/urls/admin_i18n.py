from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

admin.autodiscover()

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
)
