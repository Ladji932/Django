from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

# Définition des routes (URLs) de l'application
urlpatterns = [
    # Route pour l'interface d'administration de Django
    path('admin/', admin.site.urls),

    # Route pour la liste des articles, accessible via la racine du site
    path('', views.article_list, name='article_list'),

    # Route pour la vue de chat, accessible via /chat/
    path('chat/', views.chat_view, name='chat'),

    # Route pour l'API du chat, accessible via /chat/api/
    path('chat/api/', views.chat_api, name='chat_api'),

    # Route pour la recherche d'articles, accessible via /search/
    path('search/', views.search_articles, name='search_articles'),

    # Route pour les détails d'un article spécifique, accessible via /article/<pk>/
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
]

# Ajout de la configuration pour servir les fichiers médias en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
