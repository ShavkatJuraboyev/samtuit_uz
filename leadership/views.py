from django.shortcuts import render, get_object_or_404
from samtuit.models import Menu, Season
from django.http import JsonResponse
from samtuit.translations import TRANSLATIONS
from samtuit.views import get_menu_tree
from leadership.models import Leadership
# Create your views here.

def leader(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    leadership = Leadership.objects.filter(positions='rektor')
    substitutes = Leadership.objects.filter(positions='o\'rinbosar')

    for lead in leadership:
        lead.translated_full_name = lead.get_rek_full_name(language)
        lead.translated_position = lead.get_rek_position(language)
        
    for subs in substitutes:
        subs.translated_full_name = subs.get_rek_full_name(language)
        subs.translated_position = subs.get_rek_position(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, "season":season, 'leadership':leadership, 'substitutes':substitutes
    }

    return render(request, 'users/rektarat/raxbariyat.html', context)

def rektorat(request, slug):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    leader = get_object_or_404(Leadership, slug=slug)
    leader.translated_content = leader.get_rek_content(language)
    leader.translated_full_name = leader.get_rek_full_name(language)
    leader.translated_position = leader.get_rek_position(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, "season":season, 'leader':leader
    }
 
    return render(request, 'users/rektarat/raxbar.html', context)