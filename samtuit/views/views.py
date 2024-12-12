from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from samtuit.models.models import Post, PictureSlider, Students, Announcements, Partners
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import activate, get_language

def set_language(request):
    language = request.GET.get('lang', 'uz')  # Default til -> O'zbek
    activate(language)  # Django tarjima tizimi bilan integratsiya
    request.session['user_language'] = language
    return redirect(request.META.get("HTTP_REFERER", '/'))


def home(request):
    language = request.session.get('user_language', 'uz') 
    pictures = PictureSlider.objects.all().order_by('-id')[:7]
    posts = Post.objects.all().order_by('-id')[4:9]
    post_one = Post.objects.all().order_by('-id')[0]
    post_three = Post.objects.all().order_by('-id')[1:4]
    students = Students.objects.all()
    annos = Announcements.objects.all().order_by("-id")[:4]
    partners = Partners.objects.all()
    post_one.translated_title = post_one.get_post_title(language)  # Sarlavha
    post_one.translated_text = post_one.get_post_text(language)

    context = {'pictures':pictures, 'posts':posts, 'post_one':post_one, 'post_three':post_three, 'students':students, "annos":annos, 'partners':partners} 
    return render(request, 'users/index.html', context)

def news(request):
    language = request.session.get('user_language', 'uz')  # Default: O'zbek tili
    posts = Post.objects.all().order_by('-created_at')

    # Tanlangan tilga mos bo'lgan ma'lumotlarni o'zgartirish
    for post in posts:
        post.translated_title = post.get_post_title(language)
        post.translated_text = post.get_post_text(language)

    paginator = Paginator(posts, 6)  # Har bir sahifada 6 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    context = {'posts': paginated_posts}
    return render(request, 'users/news/news.html', context)

def new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post
    }
    return render(request, 'users/news_views/new_view.html', context)

def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.share_count += 1
    post.save()
    return JsonResponse({'share_count': post.share_count}) 

def elonlar(request):
    announcements = Announcements.objects.all()
    print(announcements)
    ctx = {'annos':announcements}
    return render(request, 'users/news/elonlar.html', ctx)

def seminarlar(request):
    return render(request, 'users/news/seminarlar.html')