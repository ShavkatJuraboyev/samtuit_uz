from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from news.models import Post, Announcements, Meeting, Details, Designation, PressConference, Seminar, Conversation
from samtuit.models import Menu, Season
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from samtuit.translations import TRANSLATIONS


def news(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    posts = Post.objects.all().order_by('-created_at')
    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    paginator = Paginator(posts, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)
    

    context = {
        'posts': paginated_posts, 'menu_text':menu_text, "menus":menus, "season":season
        }
    return render(request, 'users/news/news.html', context) 
 
def new(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    post = get_object_or_404(Post, pk=pk)
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()

    post.translated_title = post.get_post_title(language)
    post.translated_content = post.get_post_content(language)

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'menu_text':menu_text,
        "menus":menus, 'season':season
        
    }
    return render(request, 'users/news_views/new_view.html', context)

def meetings(request):  
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    meetings = Meeting.objects.all() 
    for meeting in meetings:
        meeting.translated_title = meeting.get_meeting_title(language)
        meeting.translated_text = meeting.get_meeting_text(language)

    paginator = Paginator(meetings, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    ctx = {'menu_text': menu_text, "meetings":paginated_posts, "menus":menus, 'season':season}
    return render(request, 'users/news/meetings.html', ctx)

def meeting(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    meeting = get_object_or_404(Meeting, pk=pk)
    previous_meeting = Meeting.objects.filter(id__lt=meeting.id).order_by('-id').first()
    next_meeting = Meeting.objects.filter(id__gt=meeting.id).order_by('id').first()
    meeting.translated_title = meeting.get_meeting_title(language)
    meeting.translated_content = meeting.get_meeting_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_meeting":previous_meeting, 'next_meeting':next_meeting,
        "menus":menus, 'season':season
    }
    return render(request, 'users/news_views/meeting_view.html', ctx)

def elonlar(request): 
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    announcements = Announcements.objects.all()
    for announcement in announcements:
        announcement.translated_title = announcement.get_anno_title(language)
        announcement.translated_text = announcement.get_anno_text(language)

    paginator = Paginator(announcements, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    ctx = {'annos':paginated_posts, 'menu_text':menu_text, "menus":menus, 'season':season}
    return render(request, 'users/news/elonlar.html', ctx)

def elon(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    elon = get_object_or_404(Announcements, pk=pk)
    previous_elon = Announcements.objects.filter(id__lt=elon.id).order_by('-id').first()
    next_elon = Announcements.objects.filter(id__gt=elon.id).order_by('id').first()
    elon.translated_title = elon.get_anno_title(language)
    elon.translated_content = elon.get_anno_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_elon":previous_elon, 'next_elon':next_elon,
        "menus":menus, 'season':season, 'elon':elon
    }
    return render(request, 'users/news_views/elon_view.html', ctx)


def uchrashuvlar(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    designations = Designation.objects.all()
    for designation in designations:
        designation.translated_title = designation.get_desig_title(language)
        designation.translated_text = designation.get_desig_text(language)

    paginator = Paginator(designations, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {'menu_text': menu_text, "menus":menus, 'season':season, 'desigs':paginated_posts}
    return render(request, 'users/news/uchrashuvlar.html', ctx)

def uchrashuv(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    uchrashuv = get_object_or_404(Designation, pk=pk)
    previous_uchrashuv = Designation.objects.filter(id__lt=uchrashuv.id).order_by('-id').first()
    next_uchrashuv = Designation.objects.filter(id__gt=uchrashuv.id).order_by('id').first()
    uchrashuv.translated_title = uchrashuv.get_desig_title(language)
    uchrashuv.translated_content = uchrashuv.get_desig_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_uchrashuv":previous_uchrashuv, 'next_uchrashuv':next_uchrashuv,
        "menus":menus, 'season':season, 'uchrashuv':uchrashuv
    }
    return render(request, 'users/news_views/uchrashuv_view.html', ctx)


def matbuat_anjumanlar(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    pressconferences = PressConference.objects.all()
    for pressconference in pressconferences:
        pressconference.translated_title = pressconference.get_press_title(language)
        pressconference.translated_text = pressconference.get_press_text(language)

    paginator = Paginator(pressconferences, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {'menu_text': menu_text, "menus":menus, 'season':season, 'press':paginated_posts}

    return render(request, 'users/news/matbuat_anjumanlar.html', ctx)

def matbuat_anjuman(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    matbuat_anjuman = get_object_or_404(PressConference, pk=pk)
    previous_matbuat_anjuman = PressConference.objects.filter(id__lt=matbuat_anjuman.id).order_by('-id').first()
    next_matbuat_anjuman = PressConference.objects.filter(id__gt=matbuat_anjuman.id).order_by('id').first()
    matbuat_anjuman.translated_title = matbuat_anjuman.get_press_title(language)
    matbuat_anjuman.translated_content = matbuat_anjuman.get_press_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_matbuat_anjuman":previous_matbuat_anjuman, 'next_matbuat_anjuman':next_matbuat_anjuman,
        "menus":menus, 'season':season, 'matbuat_anjuman':matbuat_anjuman
    }
    return render(request, 'users/news_views/matbuat_anjuman_view.html', ctx)

def seminarlar(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    seminars = Seminar.objects.all()
    for seminar in seminars:
        seminar.translated_title = seminar.get_semin_title(language)
        seminar.translated_text = seminar.get_semin_text(language)

    paginator = Paginator(seminars, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {'menu_text': menu_text, "menus":menus, 'season':season, 'seminars':paginated_posts}
    return render(request, 'users/news/seminarlar.html', ctx)

def seminar(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    seminar = get_object_or_404(Seminar, pk=pk)
    previous_seminar = Seminar.objects.filter(id__lt=seminar.id).order_by('-id').first()
    next_seminar = Seminar.objects.filter(id__gt=seminar.id).order_by('id').first()
    seminar.translated_title = seminar.get_semin_title(language)
    seminar.translated_content = seminar.get_semin_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_seminar":previous_seminar, 'next_seminar':next_seminar,
        "menus":menus, 'season':season, 'seminar':seminar
    }
    return render(request, 'users/news_views/seminar_view.html', ctx)


def davra_suhbatlar(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)

    conversations = Conversation.objects.all()
    for conversation in conversations:
        conversation.translated_title = conversation.get_conv_title(language)
        conversation.translated_text = conversation.get_conv_text(language)

    paginator = Paginator(conversations, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {'menu_text': menu_text, "menus":menus, 'season':season, 'convs':paginated_posts}
    return render(request, 'users/news/davra_suhbatlari.html', ctx)


def davra_suhbat(request, pk):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    conversation = get_object_or_404(Conversation, pk=pk)
    previous_conversation = Conversation.objects.filter(id__lt=conversation.id).order_by('-id').first()
    next_conversation = Conversation.objects.filter(id__gt=conversation.id).order_by('id').first()
    conversation.translated_title = conversation.get_conv_title(language)
    conversation.translated_content = conversation.get_conv_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_conversation":previous_conversation, 'next_conversation':next_conversation,
        "menus":menus, 'season':season, 'conversation':conversation
    }
    return render(request, 'users/news_views/davra_suhbat_view.html', ctx)


def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.share_count += 1
    post.save()
    return JsonResponse({'share_count': post.share_count}) 

def detail(request, slug):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children')

    for menu in menus:
        menu.translated_title = menu.get_menu_title(language)  # Asosiy menyu tarjimasi
        for child in menu.children.all():
            child.translated_title = child.get_menu_title(language)
    detail = get_object_or_404(Details, slug=slug)
    detail.translated_title = detail.get_detail_title(language)
    detail.translated_content = detail.get_detail_content(language)
    
    ctx = {'detail': detail, 'menu_text':menu_text, "menus":menus, 'season':season}
    return render(request, 'users/details/detail.html', ctx)