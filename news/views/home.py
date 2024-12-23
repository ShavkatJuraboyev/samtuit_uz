from django.shortcuts import render
from samtuit.models import Menu, ListsMenu, Lists
from django.shortcuts import get_object_or_404
from samtuit.translations import TRANSLATIONS




def menu_view(request, slug):
    language = request.session.get('django_language', 'uz')  # Hozirgi tilni oling
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    list_menu = get_object_or_404(ListsMenu, slug=slug)  # ListsMenu'ni slug bo'yicha toping
    lists = Lists.objects.filter(listmenu=list_menu)  # ListsMenu bilan bog'liq barcha Lists ma'lumotlarini oling
    list_menu.translated_title = list_menu.get_lists_title(language)

    # Tilga mos tarjimalarni qo'shing
    for lst in lists: 
        lst.translated_title = lst.get_list_title(language)
    ctx = {
        'list_menu': list_menu, 'lists': lists,
        "menu_text":menu_text, "menus":menus
        }
    return render(request, 'users/lists/list_page.html', ctx)

def view_menu_detail(request, pk):
    language = request.session.get('django_language', 'uz')  # Hozirgi tilni oling
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    list = get_object_or_404(Lists, pk=pk)
    list.translated_title = list.get_list_title(language)
    list.translated_text = list.get_list_text(language)
    list.translated_content = list.get_list_content(language)
    ctx = {
        'list': list,
        "menu_text":menu_text, "menus":menus
    }
    return render(request, 'users/lists/list_detail.html', ctx)
