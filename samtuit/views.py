from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'users/index.html')

def news(request):
    return render(request, 'users/news/news.html')