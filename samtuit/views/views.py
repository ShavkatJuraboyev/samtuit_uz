from django.shortcuts import render
from samtuit.models import Post
# Create your views here.


def home(request):
    return render(request, 'users/index.html')

def news(request):
    return render(request, 'users/news/news.html')

def new(request):
    post = Post.objects.all()
    return render(request, 'users/news/new.html', {'post':post})