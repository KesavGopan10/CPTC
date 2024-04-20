from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home , transcribe_audio , upload_file , docdet , emo
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('streamlit/', TemplateView.as_view(template_name='app/streamlit.html'), name='streamlit'),
    path('transcribe_audio', transcribe_audio, name='transcribe_audio'),
    path('upload_file', upload_file, name='upload_file'),
    path('docdet', docdet, name='docdet'),
    path('emo', emo, name='emo'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
