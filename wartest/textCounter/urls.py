from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import NewDoc, List, DocDetailView

urlpatterns = [
    path('', List.as_view(), name='index'),
    path('newDoc',NewDoc.as_view() , name='newDoc'),
    path(r'doc/<slug>', DocDetailView.as_view(), name='getDoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)