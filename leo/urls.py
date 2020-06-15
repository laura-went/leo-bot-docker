from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blob', views.get_blob, name='get_blob'),
    path('text', views.get_text, name='get_text'),
    path('casual', views.get_sentence, name='get_sentence'),
]
