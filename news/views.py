from django.shortcuts import render
from django.core.paginator import Paginator
from news.models import Post, Announcements, Meeting
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from samtuit.translations import TRANSLATIONS


def news(request):
    language = request.session.get('django_language', 'uz')  # Default: O'zbek tili
    posts = Post.objects.all().order_by('-created_at')

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    paginator = Paginator(posts, 10)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])

    context = {
        'posts': paginated_posts, 'menu_text':menu_text
        }
    return render(request, 'users/news/news.html', context) 

def new(request, pk):
    language = request.session.get('django_language', 'uz')  
    post = get_object_or_404(Post, pk=pk)
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])

    post.translated_title = post.get_post_title(language)
    post.translated_content = post.get_post_content(language)

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'menu_text':menu_text,
    }
    return render(request, 'users/news_views/new_view.html', context)


def meetings(request): 
    language = request.session.get('django_language', 'uz')
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    meetings = Meeting.objects.all() 

    ctx = {'menu_text': menu_text, "meetings":meetings}
    return render(request, 'users/news/meetings.html', ctx)

def meeting(request, pk):
    language = request.session.get('django_language', 'uz') 
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])
    meeting = get_object_or_404(Meeting, pk=pk)
    previous_post = Post.objects.filter(id__lt=meeting.id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=meeting.id).order_by('id').first()
    meeting.translated_title = meeting.get_meeting_title(language)
    meeting.translated_content = meeting.get_meeting_content(language)

    ctx = {
        "menu_text":menu_text, "meeting":meeting,
        "previous_post":previous_post, 'next_post':next_post,
    }
    return render(request, 'users/news_views/meeting_view.html')



def elonlar(request):
    language = request.session.get('django_language', 'uz')
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])

    announcements = Announcements.objects.all()
    print(announcements)
    ctx = {'annos':announcements, 'menu_text':menu_text}
    return render(request, 'users/news/elonlar.html', ctx)

def uchrashuvlar(request):
    language = request.session.get('django_language', 'uz')
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['uz'])

    ctx = {'menu_text': menu_text}
    return render(request, 'users/news/uchrashuvlar.html', ctx)

def matbuat_anjumanlar(request):
    return render(request, 'users/news/matbuat_anjumanlar.html')

def seminarlar(request):
    return render(request, 'users/news/seminarlar.html')

def davra_suhbatlar(request):
    return render(request, 'users/news/davra_suhbatlari.html')


def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.share_count += 1
    post.save()
    return JsonResponse({'share_count': post.share_count}) 
