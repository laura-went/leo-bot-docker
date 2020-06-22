# from django.conf.urls import include
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/favicon/favicon.ico')),
    path('', include('leo.urls')),
]
