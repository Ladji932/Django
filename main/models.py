from django.db import models
from django.utils.translation import gettext_lazy as _

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Publication Date"))
    custom_id = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='article_images/', null=True, blank=True, verbose_name=_("Image"))

    def __str__(self):
        return self.title
