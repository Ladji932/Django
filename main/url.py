from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.article_list, name='article_list'),  
    path('chat/', views.chat_view, name='chat'),  
    path('chat/api/', views.chat_api, name='chat_api'),  
    path('search/', views.search_articles, name='search_articles'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
