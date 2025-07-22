from django.shortcuts import render, redirect
from samtuit.models import PictureSlider, Students, Partners, Wisdom, Menu, Season, QuickMmenu
from news.models import Post, Announcements
from django.utils.translation import activate
from samtuit.translations import TRANSLATIONS
from samtuit.forms import ContactForm, ForeignStudentForm
from django.contrib import messages
from django.utils.translation import get_language
from interaktiv.models import ForeignStudent


def set_language(request):
    language = request.GET.get('lang', 'uz')  # Default til
    activate(language)  # Tarjima tizimini o'zgartirish
    response = redirect(request.META.get("HTTP_REFERER", '/'))  # Oldingi sahifaga qaytish
    response.set_cookie('django_language', language)  # Cookie o'rnatish
    return response

def get_menu_tree(menu, language):
    """
    Rekursiv menyu daraxtini yaratadi.
    """
    menu_data = {
        'id': menu.id,
        'title': menu.get_menu_title(language),
        'url': menu.url,
        'children': [get_menu_tree(child, language) for child in menu.children.all()]
    }
    return menu_data

def home(request): 
    language = get_language()
    pictures = PictureSlider.objects.all().order_by('-id')[:4]
    post_one = Post.objects.all().order_by('-created_at').first()
    post_three = Post.objects.all().order_by('-created_at')[1:5]
    for post in post_three:
        post.translated_title = post.get_post_title(language)
    students = Students.objects.all()
    annos = Announcements.objects.all().order_by("-id")[:4]
    for ann in annos:
        ann.translated_title = ann.get_anno_title(language)
        ann.translated_text = ann.get_anno_text(language)
    partners = Partners.objects.all() 
    
    post_one.translated_title = post_one.get_post_title(language)  # Sarlavha
    post_one.translated_text = post_one.get_post_text(language)
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])

    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    
    wisdoms = Wisdom.objects.all().order_by("-id")[:5]
    for wisdom in wisdoms:
        wisdom.translated_title = wisdom.get_wis_title(language)
        wisdom.translated_text = wisdom.get_wis_text(language)

    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    season = Season.objects.all().order_by("-id").first()

    context = {
        'pictures':pictures, 
        'post_one':post_one, 'post_three':post_three, 
        'students':students, "annos":annos, 
        'partners':partners, 'menu_text':menu_text,
        'wisdoms':wisdoms, 
        'menus':menu_tree, 'season':season, 'quickmmenu':quickmmenu, "language":language
        } 
    return render(request, 'users/index.html', context)

def contact(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Ma'lumotlarni bazaga saqlash
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
            return redirect('contact')  # Kontakt sahifasiga qaytish
        else:
            messages.error(request, "Xatolik yuz berdi. Iltimos, ma'lumotlarni to'g'ri kiriting.")
    else:
        form = ContactForm()

    ctx = {
        'menu_text':menu_text, 
        "menus":menu_tree, 'season':season, 
        'quickmmenu':quickmmenu, 
        'language':language,
        "form": form
        }
    return render(request, 'users/contact.html', ctx)

def site_map(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    ctx = {
        'menu_text':menu_text, 
        "menus":menu_tree, 'season':season, 
        'quickmmenu':quickmmenu, 
        'language':language
        }
    return render(request, 'users/site_map.html', ctx)


def student(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    ctx = {
        'menu_text':menu_text, 
        "menus":menu_tree, 'season':season, 
        'quickmmenu':quickmmenu, 
        'language':language
        }
    return render(request, 'users/student.html', ctx)

def foreign_student(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)
    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    if request.method == "POST":
        form = ForeignStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('foreign_student')
        else:
            messages.error(request, "There was an error. Please check your information.")
    else:
        form = ForeignStudentForm()

    foreign_students = ForeignStudent.objects.all()

    ctx = {
        'menu_text': menu_text,
        "menus": menu_tree,
        'season': season,
        'quickmmenu': quickmmenu,
        'language': language,
        'foreign_students': foreign_students,
        'form': form
    }
    return render(request, 'users/foreign_student.html', ctx)