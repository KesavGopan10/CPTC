from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home , transcribe_audio

urlpatterns = [
    path('', home, name='home'),
    path('transcribe_audio', transcribe_audio, name='transcribe_audio'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
