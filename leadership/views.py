from django.shortcuts import render, get_object_or_404
from samtuit.models import Menu, Season, QuickMmenu
from news.models import Post
from samtuit.translations import TRANSLATIONS
from samtuit.views import get_menu_tree
from leadership.models import Leadership, Departments, DepartmentsCenter, Faculty, FacultyDean
from django.utils.translation import get_language
# Create your views here.

def leader(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    leadership = Leadership.objects.filter(positions='rektor')
    substitutes = Leadership.objects.filter(positions='o\'rinbosar')

    for lead in leadership:
        lead.translated_full_name = lead.get_rek_full_name(language)
        lead.translated_position = lead.get_rek_position(language)
        
    for subs in substitutes:
        subs.translated_full_name = subs.get_rek_full_name(language)
        subs.translated_position = subs.get_rek_position(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'leadership':leadership, 'substitutes':substitutes, 'next_posts': posts, 'language':language
    }

    return render(request, 'users/rektarat/raxbariyat.html', context)

def rektorat(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    leader = get_object_or_404(Leadership, slug=slug)
    leader.translated_content = leader.get_rek_content(language)
    leader.translated_full_name = leader.get_rek_full_name(language)
    leader.translated_position = leader.get_rek_position(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'leader':leader, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/raxbar.html', context)

def kafedralar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    title_field = f"titul_{language}"
    kafedra = Departments.objects.all().order_by(title_field)
    for kaf in kafedra:
        kaf.translated_title = kaf.get_dep_titul(language)
        kaf.translated_text = kaf.get_dep_text(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'kafedra':kafedra, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/kafedralar.html', context)

def kafedra(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    kafedr = get_object_or_404(Departments, slug=slug)
    kafedr.translated_content = kafedr.get_dep_content(language)
    kafedr.translated_title = kafedr.get_dep_titul(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'kafedr':kafedr, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/kafedra.html', context)

def markazlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    title_field = f"title_{language}"
    center = DepartmentsCenter.objects.all().order_by(title_field)
    for kaf in center:
        kaf.translated_title = kaf.get_depcen_title(language)
        kaf.translated_text = kaf.get_depcen_text(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'leader':leader, 'kafedra':center, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/markazlar.html', context)

def markaz(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    center = get_object_or_404(DepartmentsCenter, slug=slug)
    center.translated_content = center.get_depcen_content(language)
    center.translated_title = center.get_depcen_title(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'kafedr':center, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/markaz.html', context)

def fakultetlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    faculty = Faculty.objects.all().order_by('-id')
    for facul in faculty:
        facul.translated_title = facul.get_facul_titul(language)
        facul.translated_text = facul.get_facul_text(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'faculty':faculty, 'next_posts': posts, 'language':language
    }
 
    return render(request, 'users/rektarat/facultetlar.html', context)

def fakultet(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    fakultet = get_object_or_404(Faculty, slug=slug)
    dekanlar = [
        {
        'full_name':dekan.get_dekan_full_name(language),
        'image':dekan.get_dekan_img,
        'acceptance':dekan.acceptance,
        'phone':dekan.phone,
        'email':dekan.email,
        'positions':dekan.positions,
        'faculty':dekan.faculty,
        'created_at':dekan.created_at,
        'created_by':dekan.created_by,
        'content':dekan.get_dekan_content(language),
        'position':dekan.get_dekan_position(language),
        'slug':dekan.slug
        }
        for dekan in fakultet.dekanlar.all()
    ]
    kafedralar = [
        {
            'titul':kafedra.get_dep_titul(language),
            'text':kafedra.get_dep_text(language),
            'slug':kafedra.slug
        }
        for kafedra in fakultet.kafedra.all()
    ]
    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'dekanlar': dekanlar, 'kafedralar':kafedralar, 'next_posts': posts, 'language':language
        }

    return render(request, 'users/rektarat/fakultet.html', context)

def dekan(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    dekan = get_object_or_404(FacultyDean, slug=slug)
    dekan.translated_content = dekan.get_dekan_content(language)
    dekan.translated_full_name = dekan.get_dekan_full_name(language)
    dekan.translated_position = dekan.get_dekan_position(language)

    context = {
        'menu_text':menu_text, "menus":menu_tree, 
        "season":season, 'quickmmenu':quickmmenu, 
        'dekan':dekan, 'next_posts': posts, 'language':language 
        }

    return render(request, 'users/rektarat/dekan.html', context)