from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/get_random_words", views.get_random_words),
    path("api/get_random_sentences", views.get_random_sentences),
    path("api/get_audio", views.get_audio),
    path("api/compare_sentences", views.compare_sentences),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
