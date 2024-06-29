from django.contrib import admin
from .models import Article

# J'enregistre le modèle Article avec l'interface d'administration de Django
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Je définit les champs à afficher dans la liste des articles dans l'interface d'administration
    list_display = ('title', 'publication_date', 'custom_id', 'content')
