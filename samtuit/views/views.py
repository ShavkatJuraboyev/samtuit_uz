from django.shortcuts import render
from django.core.paginator import Paginator
from samtuit.models import Post, PictureSlider
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def home(request):
    pictures = PictureSlider.objects.all()
    posts = Post.objects.all().order_by('-id')[:6]
    context = {'pictures':pictures, 'posts':posts} 
    return render(request, 'users/index.html', context)

def news(request):
    post = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post, 6) 

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {'posts': posts}
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
    return render(request, 'users/news/new.html', context)

def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.share_count += 1
    post.save()
    return JsonResponse({'share_count': post.share_count}) 