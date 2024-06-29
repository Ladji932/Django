from django.db import models
from django.utils.translation import gettext_lazy as _

# Définition du modèle Article
class Article(models.Model):
    # Champ pour le titre de l'article, limité à 200 caractères
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    
    # Champ pour le contenu de l'article, sans limite de caractères
    content = models.TextField(verbose_name=_("Content"))
    
    # Champ pour la date de publication, auto-rempli à la création de l'article
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Publication Date"))
    
    # Champ pour un identifiant personnalisé, unique et limité à 100 caractères
    custom_id = models.CharField(max_length=100, unique=True)
    
    # Champ pour une image associée à l'article, optionnelle
    image = models.ImageField(upload_to='article_images/', null=True, blank=True, verbose_name=_("Image"))

    # Méthode pour retourner le titre de l'article comme représentation en chaîne de caractères
    def __str__(self):
        return self.title
