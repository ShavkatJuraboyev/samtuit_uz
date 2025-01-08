from django.shortcuts import render
from samtuit.models import Menu, ListsMenu, Lists, QuickMmenu
from django.shortcuts import get_object_or_404
from samtuit.translations import TRANSLATIONS
from samtuit.views import get_menu_tree

def get_nested_children(list_menu):
    children = list_menu.children.all()
    return [{
        'list_menu': child,
        'children': get_nested_children(child)
    } for child in children]

def menu_view(request, slug):
    language = request.session.get('django_language', 'uz')  # Hozirgi tilni oling
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    list_menu = get_object_or_404(ListsMenu, slug=slug)  # ListsMenu'ni slug bo'yicha toping
    nested_children = get_nested_children(list_menu)

    lists = Lists.objects.filter(listmenu=list_menu)  # ListsMenu bilan bog'liq barcha Lists ma'lumotlarini oling
    # Tilga mos tarjimalarni qo'shing
    for lst in lists: 
        lst.translated_title = lst.get_list_title(language)
    ctx = {
        'list_menu': list_menu, 'lists': lists,
        "menu_text":menu_text, "menus":menu_tree, 'children': nested_children,
        'quickmmenu':quickmmenu
        }
    return render(request, 'users/lists/list_page.html', ctx)

def view_menu_detail(request, pk):
    language = request.session.get('django_language', 'uz')  # Hozirgi tilni oling
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    list = get_object_or_404(Lists, pk=pk)
    list.translated_title = list.get_list_title(language)
    list.translated_text = list.get_list_text(language)
    list.translated_content = list.get_list_content(language)
    ctx = {
        'list': list,
        "menu_text":menu_text, "menus":menu_tree,
        'quickmmenu':quickmmenu
    }
    return render(request, 'users/lists/list_detail.html', ctx)

