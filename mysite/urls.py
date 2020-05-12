# from django.conf.urls import include
from django.urls import include, path

urlpatterns = [
    path('', include('leo.urls')),
]
# urlpatterns += static(r'/favicon.ico', document_root='static/favicon.ico')
