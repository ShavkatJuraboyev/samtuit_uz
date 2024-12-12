from django.shortcuts import render
from django.core.paginator import Paginator
from samtuit.models.models import Post, PictureSlider, Students, Announcements
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



def davra_suhbatlar(request):
    return render(request, 'users/news/davra_suhbatlari.html')

def matbuat_anjumanlar(request):
    return render(request, 'users/news/matbuat_anjumanlar.html')

def meetings(request): 
    return render(request, 'users/news/meetings.html')

def uchrashuvlar(request):
    return render(request, 'users/news/uchrashuvlar.html')

