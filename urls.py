from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/fetch_all_themes", views.fetch_all_themes),
    path("api/fetch_theme_pages", views.fetch_theme_pages),
    path("api/fetch_page_blocks", views.fetch_page_blocks),
    path("api/check_theme_existence", views.check_theme_existence),
    path("api/perform_category_search", views.perform_category_search),
    path("api/fetch_next_subcategories_or_data", views.fetch_next_subcategories_or_data),
    #path("api/dynamic_search", views.dynamic_search),
    path("api/delete_theme", views.delete_theme),
    #path("api/get_table_names", views.get_table_names),
    #path("api/get_table_data", views.get_table_data),
    #path("api/get_image", views.get_image),
    #path("api/get_audio", views.get_audio),
    #path("api/get_video", views.get_video),
    path("api/save_theme", views.save_theme),
    path("api/save_page", views.save_page),
    path("api/delete_page", views.delete_page),
    path("api/delete_blocks", views.delete_blocks),
    #path("api/fetch_all_pages", views.fetch_all_pages),
    path("api/compare_sentences", views.compare_sentences),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
