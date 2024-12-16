from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from samtuit.models import PictureSlider, Students, Partners, Wisdom, Celebrities
from django.shortcuts import get_object_or_404
from news.models import Post, Announcements
from django.utils.translation import activate
from samtuit.translations import TRANSLATIONS
from django.db.models import Prefetch



def set_language(request):
    language = request.GET.get('lang', 'uz')  # Default til
    activate(language)  # Tarjima tizimini o'zgartirish
    request.session['django_language'] = language  # Sessiyada tilni saqlash
    response = redirect(request.META.get("HTTP_REFERER", '/'))  # Oldingi sahifaga qaytish
    response.set_cookie('django_language', language)  # Cookie o'rnatish
    return response


def home(request):
    language = request.session.get('django_language', 'uz') 
    pictures = PictureSlider.objects.all().order_by('-id')[:7]
    posts = Post.objects.all().order_by('-id')[4:9]
    post_one = Post.objects.all().order_by('-id')[0]
    post_three = Post.objects.all().order_by('-id')[1:4]
    students = Students.objects.all()
    annos = Announcements.objects.all().order_by("-id")[:4]
    partners = Partners.objects.all()
    
    post_one.translated_title = post_one.get_post_title(language)  # Sarlavha
    post_one.translated_text = post_one.get_post_text(language)
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    
    wisdoms = Wisdom.objects.all().order_by("-id")[:5]
    for wisdom in wisdoms:
        wisdom.translated_title = wisdom.get_wis_title(language)
        wisdom.translated_text = wisdom.get_wis_text(language)
    
    celebrities = Celebrities.objects.all().order_by("-id")[:3]
    for celebritie in celebrities:
        celebritie.translated_title = celebritie.get_cel_title(language)
        celebritie.translated_text = celebritie.get_cel_text(language)

    context = {
        'pictures':pictures, 'posts':posts, 
        'post_one':post_one, 'post_three':post_three, 
        'students':students, "annos":annos, 
        'partners':partners, 'menu_text':menu_text,
        'wisdoms':wisdoms, 'celebrities':celebrities,
        } 
    return render(request, 'users/index.html', context)