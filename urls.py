from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/fetch_all_pages", views.fetch_all_pages),
    path("api/fetch_page_blocks", views.fetch_page_blocks),
    path("api/check_page_existence", views.check_page_existence),
    path("api/dynamic_search", views.dynamic_search),
    path("api/get_table_names", views.get_table_names),
    path("api/get_table_data", views.get_table_data),
    path("api/fetch_files", views.fetch_files),
    path("api/save_page", views.save_page),
    path("api/fetch_all_pages", views.fetch_all_pages),
    path("api/fetch_page_blocks", views.fetch_page_blocks),
    path("api/compare_sentences", views.compare_sentences),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
