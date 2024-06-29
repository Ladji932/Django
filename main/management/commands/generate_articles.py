from django.core.management.base import BaseCommand
from main.models import Article
from django.utils import timezone
from django.utils.translation import gettext as _
from faker import Faker
import random
import uuid

class Command(BaseCommand):
    help = 'Generate fake articles'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(10):
            title_en = fake.sentence(nb_words=4, variable_nb_words=True)
            content_en = fake.paragraph(nb_sentences=random.randint(5, 15))
            
            title_fr = _(title_en)  # Traduction du titre en français
            content_fr = _(content_en)  # Traduction du contenu en français
            
            article = Article(
                title=title_en,
                content=content_en,
                title_fr=title_fr,
                content_fr=content_fr,
                publication_date=timezone.now(),
                custom_id=str(uuid.uuid4()),  # Générer un identifiant unique
            )
            article.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 articles'))
