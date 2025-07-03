from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from news.models import Post, Announcements, Meeting, Details, Designation, PressConference, Seminar, Conversation
from samtuit.models import Menu, Season, QuickMmenu
from django.http import JsonResponse
from samtuit.translations import TRANSLATIONS
from samtuit.views import get_menu_tree
from django.utils.translation import get_language


def news(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    # Sahifalash
    paginator = Paginator(posts, 6)  # Har bir sahifada 5 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    # Joriy sahifadagi postlar uchun keyingi 5 ta postni olish
    start_index = paginated_posts.end_index()  # Joriy sahifaning oxirgi postining indeksini olish

    # Agar oxirgi sahifaga yetilgan bo'lsa, keyingi postlarni boshidan olish
    if start_index >= len(posts):  
        remaining_posts_count = len(posts)  # Qolgan postlar sonini olish
        next_posts = posts[:8]  # Postlar ro'yxatining boshidan 5 ta postni olish
        # Qolgan postlarni to'ldirish uchun yana boshidan postlarni olish
        if remaining_posts_count < 8:
            next_posts.extend(posts[remaining_posts_count:remaining_posts_count + (5 - remaining_posts_count)])
    else:
        next_posts = posts[start_index:start_index + 8]  # Joriy postdan keyingi 5 ta postni olish

    # Keyingi 5 ta postni tarjima qilish
    for next_post_item in next_posts:
        next_post_item.translated_title = next_post_item.get_post_title(language)
        next_post_item.translated_text = next_post_item.get_post_text(language)
    

    context = {
        'posts': paginated_posts, 'menu_text':menu_text, 'language':language,
        "menus":menu_tree, "season":season, 'quickmmenu':quickmmenu,
        'next_posts': next_posts,
        }
    return render(request, 'users/news/news.html', context) 
 
def new(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    menu_tree = [get_menu_tree(menu, language) for menu in menus]
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)


    post = get_object_or_404(Post, pk=pk)  # Joriy postni olish

    # Oldingi va keyingi postlarni olish
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()

    # Barcha postlarni olish tartiblangan holda
    posts = list(Post.objects.all().order_by('id'))

    # Joriy postning indeksini olish
    current_index = posts.index(post)

    # Keyingi 5 ta postni olish
    next_posts = []
    for i in range(1, 8):
        next_index = (current_index + i) % len(posts)  # Oxiridan keyin boshiga o'tish
        next_posts.append(posts[next_index])

    # Keyingi postlarni tarjima qilish
    for next_post_item in next_posts:
        next_post_item.translated_title = next_post_item.get_post_title(language)
        next_post_item.translated_text = next_post_item.get_post_text(language)

    # Post ma'lumotlarini tarjima qilish
    post.translated_title = post.get_post_title(language)
    post.translated_content = post.get_post_content(language)


    

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'menu_text':menu_text, 'language':language,
        "menus":menu_tree, 'season':season, 
        'quickmmenu':quickmmenu,
        'next_posts': next_posts,
    }
    return render(request, 'users/news_views/new_view.html', context)

def meetings(request):  
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    meetings = Meeting.objects.all() 
    for meeting in meetings:
        meeting.translated_title = meeting.get_meeting_title(language)
        meeting.translated_text = meeting.get_meeting_text(language)

    paginator = Paginator(meetings, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    ctx = {
        'menu_text': menu_text, 'language':language, "meetings":paginated_posts, 
        "menus":menu_tree, 'season':season, 'quickmmenu':quickmmenu,
        'next_posts': posts,
        }
    return render(request, 'users/news/meetings.html', ctx)

def meeting(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    meeting = get_object_or_404(Meeting, pk=pk)
    previous_meeting = Meeting.objects.filter(id__lt=meeting.id).order_by('-id').first()
    next_meeting = Meeting.objects.filter(id__gt=meeting.id).order_by('id').first()
    meeting.translated_title = meeting.get_meeting_title(language)
    meeting.translated_content = meeting.get_meeting_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_meeting":previous_meeting, 'next_meeting':next_meeting,
        "menus":menu_tree, 'season':season, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/meeting_view.html', ctx)

def elonlar(request): 
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    announcements = Announcements.objects.all()
    for announcement in announcements:
        announcement.translated_title = announcement.get_anno_title(language)
        announcement.translated_text = announcement.get_anno_text(language)

    paginator = Paginator(announcements, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    ctx = {
        'annos':paginated_posts, 'menu_text':menu_text, 'language':language, 
        "menus":menu_tree, 'season':season, 'quickmmenu':quickmmenu,
        'next_posts': posts,}
    return render(request, 'users/news/elonlar.html', ctx)

def elon(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    elon = get_object_or_404(Announcements, pk=pk)
    previous_elon = Announcements.objects.filter(id__lt=elon.id).order_by('-id').first()
    next_elon = Announcements.objects.filter(id__gt=elon.id).order_by('id').first()
    elon.translated_title = elon.get_anno_title(language)
    elon.translated_content = elon.get_anno_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_elon":previous_elon, 'next_elon':next_elon,
        "menus":menu_tree, 'season':season, 'elon':elon, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/elon_view.html', ctx)

def uchrashuvlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    designations = Designation.objects.all()
    for designation in designations:
        designation.translated_title = designation.get_desig_title(language)
        designation.translated_text = designation.get_desig_text(language)

    paginator = Paginator(designations, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {
        'menu_text': menu_text, 'language':language, "menus":menu_tree, 
        'season':season, 'desigs':paginated_posts, 
        'quickmmenu':quickmmenu, 'next_posts': posts,}
    return render(request, 'users/news/uchrashuvlar.html', ctx)

def uchrashuv(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    uchrashuv = get_object_or_404(Designation, pk=pk)
    previous_uchrashuv = Designation.objects.filter(id__lt=uchrashuv.id).order_by('-id').first()
    next_uchrashuv = Designation.objects.filter(id__gt=uchrashuv.id).order_by('id').first()
    uchrashuv.translated_title = uchrashuv.get_desig_title(language)
    uchrashuv.translated_content = uchrashuv.get_desig_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_uchrashuv":previous_uchrashuv, 'next_uchrashuv':next_uchrashuv,
        "menus":menu_tree, 'season':season, 'uchrashuv':uchrashuv, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/uchrashuv_view.html', ctx)

def matbuat_anjumanlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    pressconferences = PressConference.objects.all()
    for pressconference in pressconferences:
        pressconference.translated_title = pressconference.get_press_title(language)
        pressconference.translated_text = pressconference.get_press_text(language)

    paginator = Paginator(pressconferences, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {
        'menu_text': menu_text, 'language':language, "menus":menu_tree, 
        'season':season, 'press':paginated_posts, 
        'quickmmenu':quickmmenu, 'next_posts': posts,}

    return render(request, 'users/news/matbuat_anjumanlar.html', ctx)

def matbuat_anjuman(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    matbuat_anjuman = get_object_or_404(PressConference, pk=pk)
    previous_matbuat_anjuman = PressConference.objects.filter(id__lt=matbuat_anjuman.id).order_by('-id').first()
    next_matbuat_anjuman = PressConference.objects.filter(id__gt=matbuat_anjuman.id).order_by('id').first()
    matbuat_anjuman.translated_title = matbuat_anjuman.get_press_title(language)
    matbuat_anjuman.translated_content = matbuat_anjuman.get_press_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_matbuat_anjuman":previous_matbuat_anjuman, 'next_matbuat_anjuman':next_matbuat_anjuman,
        "menus":menu_tree, 'season':season, 'matbuat_anjuman':matbuat_anjuman, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/matbuat_anjuman_view.html', ctx)

def seminarlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    seminars = Seminar.objects.all()
    for seminar in seminars:
        seminar.translated_title = seminar.get_semin_title(language)
        seminar.translated_text = seminar.get_semin_text(language)

    paginator = Paginator(seminars, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {
        'menu_text': menu_text, 'language':language, "menus":menu_tree, 
        'season':season, 'seminars':paginated_posts, 
        'quickmmenu':quickmmenu, 'next_posts': posts,}
    return render(request, 'users/news/seminarlar.html', ctx)

def seminar(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    seminar = get_object_or_404(Seminar, pk=pk)
    previous_seminar = Seminar.objects.filter(id__lt=seminar.id).order_by('-id').first()
    next_seminar = Seminar.objects.filter(id__gt=seminar.id).order_by('id').first()
    seminar.translated_title = seminar.get_semin_title(language)
    seminar.translated_content = seminar.get_semin_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_seminar":previous_seminar, 'next_seminar':next_seminar,
        "menus":menu_tree, 'season':season, 'seminar':seminar, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/seminar_view.html', ctx)

def davra_suhbatlar(request):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    conversations = Conversation.objects.all()
    for conversation in conversations:
        conversation.translated_title = conversation.get_conv_title(language)
        conversation.translated_text = conversation.get_conv_text(language)

    paginator = Paginator(conversations, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)


    ctx = {
        'menu_text': menu_text, 'language':language, "menus":menu_tree, 
        'season':season, 'convs':paginated_posts, 
        'quickmmenu':quickmmenu,'next_posts': posts,}
    return render(request, 'users/news/davra_suhbatlari.html', ctx)

def davra_suhbat(request, pk):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    conversation = get_object_or_404(Conversation, pk=pk)
    previous_conversation = Conversation.objects.filter(id__lt=conversation.id).order_by('-id').first()
    next_conversation = Conversation.objects.filter(id__gt=conversation.id).order_by('id').first()
    conversation.translated_title = conversation.get_conv_title(language)
    conversation.translated_content = conversation.get_conv_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_conversation":previous_conversation, 'next_conversation':next_conversation,
        "menus":menu_tree, 'season':season, 'conversation':conversation, 'quickmmenu':quickmmenu,
        'next_posts': posts,
    }
    return render(request, 'users/news_views/davra_suhbat_view.html', ctx)

def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.share_count += 1
    post.save()
    return JsonResponse({'share_count': post.share_count}) 

def detail(request, slug):
    language = get_language()  # Default: O'zbek tili
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    season = Season.objects.all().order_by("-id").first()
    menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    quickmmenu = QuickMmenu.objects.all()[:7]
    for quic in quickmmenu:
        quic.translated_title = quic.get_menu_title(language)

    menu_tree = [get_menu_tree(menu, language) for menu in menus]

    posts = Post.objects.all().order_by('-created_at')[:8]  # Postlar ro'yxatini yaratish

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    detail = get_object_or_404(Details, slug=slug)
    detail.translated_title = detail.get_detail_title(language)
    detail.translated_content = detail.get_detail_content(language)
    
    ctx = {
        'detail': detail, 'menu_text':menu_text, 'language':language, 
        "menus":menu_tree, 'season':season, 
        'quickmmenu':quickmmenu, 'next_posts': posts,}
    return render(request, 'users/details/detail.html', ctx)