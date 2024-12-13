from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from samtuit.models.models import PictureSlider, Students, Partners, Menu
from django.shortcuts import get_object_or_404
from news.models import Post, Announcements, Meeting
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
    
    menus = Menu.objects.all()
    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)

    context = {
        'pictures':pictures, 'posts':posts, 
        'post_one':post_one, 'post_three':post_three, 
        'students':students, "annos":annos, 
        'partners':partners, 'menu_text':menu_text,
        'menus':menus
        } 
    return render(request, 'users/index.html', context)