from django.urls import path
from . import views

urlpatterns = [path("api/get_random_words", views.get_random_words),
               path("api/get_random_sentences", views.get_random_sentences),
               path("api/get_audio", views.get_audio),
                path("api/compare_sentences",views.compare_sentences)]