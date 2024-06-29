# views.py
from django.shortcuts import render, get_object_or_404
from django.utils.translation import activate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone

from .models import Article

# Charger le modèle DialoGPT et le tokenizer pour le français
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

from faker import Faker
import random
import uuid
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# Configuration du logger
logger = logging.getLogger(__name__)

model_name = "microsoft/DialoGPT-small"  # Changez ceci si un modèle spécifique pour le français est trouvé
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_random_articles():
    fake = Faker()

    titles = [fake.sentence(nb_words=4, variable_nb_words=True) for _ in range(10)]
    contents = [fake.paragraph(nb_sentences=random.randint(5, 15)) for _ in range(10)]
    articles = []

    for i in range(10):
        # Télécharger une image aléatoire depuis l'URL de Faker
        image_url = fake.image_url(width=800, height=600)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(requests.get(image_url).content)
        img_temp.flush()

        article = Article(
            title=titles[i],
            content=contents[i],
            publication_date=timezone.now(),
            custom_id=str(uuid.uuid4()),  # Générer un identifiant unique
        )
        article.image.save(f'random_image_{i}.jpg', File(img_temp))

        articles.append(article)

    return articles

def article_list(request):
    lang_code = request.GET.get('lang', 'fr')  # La langue par défaut est 'en'
    activate(lang_code)  # Activez la langue sélectionnée

    # Générer les articles avec les images aléatoires
    articles = generate_random_articles()

    return render(request, 'main/article_list.html', {'articles': articles})

def article_detail(request, pk):
    lang_code = request.GET.get('lang', 'fr')  # La langue par défaut est 'en'
    activate(lang_code)  # Activez la langue sélectionnée
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'main/article_detail.html', {'article': article})

@csrf_exempt
def search_articles(request):
    
    
    if request.method == 'GET':
        query = request.GET.get('q', '')

        if not query:
            return render(request, 'main/results.html', {'error': 'Requête de recherche vide'})

        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        articles_data = [{'title': article.title, 'content': article.content[:200], 'image_url': article.image.url} for article in articles]

        try:
            # Construire le prompt pour le modèle DialoGPT
            prompt = f"Voici des articles de blog trouvés pour la recherche '{query}' :\n"
            for article in articles_data:
                prompt += f"Titre : {article['title']}\nContenu : {article['content']}...\n\n"
            prompt += "\nGénérer un résumé et des suggestions supplémentaires pour ces résultats de recherche."

            # Limiter la longueur du prompt
            max_input_length = 1000  # Ajuster selon les besoins
            if len(tokenizer.encode(prompt)) > max_input_length:
                prompt = tokenizer.decode(tokenizer.encode(prompt)[:max_input_length], skip_special_tokens=True)

            # Encoder le prompt pour le modèle
            input_ids = tokenizer.encode(prompt, return_tensors='pt')

            # Générer la réponse avec le modèle DialoGPT
            with torch.no_grad():
                response_ids = model.generate(input_ids, max_new_tokens=300, num_return_sequences=1)

            # Décoder la réponse générée par le modèle
            enhanced_response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

            # Passer les résultats et la réponse améliorée au template
            return render(request, 'main/results.html', {'results': articles_data, 'enhanced': enhanced_response})

        except Exception as e:
            # Capturer et loguer les erreurs
            error_msg = f"Erreur dans l'augmentation des résultats avec DialoGPT: {str(e)}"
            logger.error(error_msg)
            return render(request, 'main/results.html', {'error': error_msg})

    return render(request, 'main/results.html', {'error': 'Requête invalide'})


def chat_view(request):
    return render(request, 'main/chat.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        print(user_message)
        
        try:
            user_message = user_message.strip()
            user_message = ' '.join(user_message.split())

            input_ids = tokenizer.encode(user_message, return_tensors='pt')

            with torch.no_grad():
                response_ids = model.generate(
                    input_ids, 
                    max_length=100, 
                    do_sample=True,   
                    top_k=50, 
                    top_p=0.95, 
                    temperature=0.7,   # Ajuster la température
                    num_return_sequences=1                
                )
            
            chatbot_response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
            
            # Validation de la réponse générée
            if not chatbot_response.strip():
                chatbot_response = "Désolé, je n'ai pas pu comprendre votre question."

            return JsonResponse({'response': chatbot_response})

        except Exception as e:
            # Enregistrer l'erreur et retourner une réponse JSON avec les détails de l'erreur
            error_msg = f"Erreur dans la génération de réponse avec DialoGPT: {str(e)}"
            logger.error(error_msg)
            return JsonResponse({'error': error_msg}, status=500)

    return JsonResponse({'error': 'Requête invalide'}, status=400)


