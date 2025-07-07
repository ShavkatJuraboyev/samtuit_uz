import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from interaktiv.models import UserHemis, GrantApplication
from django.contrib.auth.decorators import login_required 
from datetime import datetime


def get_user_info(hemis_id):
    """Hemis id kiritilishi lozim"""
    url = f"https://student.samtuit.uz/rest/v1/data/student-info?student_id_number={hemis_id}"
    token = "Y-R36P1BY-eLfuCwQbcbAlvt9GAMk-WP"
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def login(request):
    if request.method == "POST":
        login_type = request.POST.get("login_type")

        if login_type == "local":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                django_login(request, user)
                return redirect('admins')  # foydalanuvchi kirgandan keyin yo'naltiriladigan sahifa
            else:
                messages.error(request, "Login yoki parol noto‘g‘ri")

        elif login_type == "hemis":
            return redirect(
                f"{settings.HEMIS_OAUTH2_AUTHORIZATION_URL}?client_id={settings.HEMIS_OAUTH2_CLIENT_ID}"
                f"&redirect_uri={settings.HEMIS_REDIRECT_URI}&response_type=code"
            )

    return render(request, 'interaktiv/login.html')

def callback(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Kod mavjud emas.')
        return redirect('login_oauth')

    token_response = requests.post(settings.HEMIS_OAUTH2_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.HEMIS_REDIRECT_URI,
        'client_id': settings.HEMIS_OAUTH2_CLIENT_ID,
        'client_secret': settings.HEMIS_OAUTH2_CLIENT_SECRET,
    })

    if token_response.status_code != 200:
        messages.error(request, 'Token olishda xato.')
        return redirect('login_oauth')

    token_data = token_response.json()
    access_token = token_data.get('access_token')
    request.session['access_token'] = access_token
    # request.session['hemis_authenticated'] = True

    # Foydalanuvchi ma'lumotlarini olish
    user_info_response = requests.get(settings.HEMIS_OATUHT2_API_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })

    if user_info_response.status_code != 200:
        messages.error(request, 'Foydalanuvchi maʼlumotlarini olishda xatolik.')
        return redirect('login_oauth')

    user_info = user_info_response.json()
    data = user_info.get('data', {})

    hemis_id = data.get('student_id_number')
    phone = data.get('phone', '')
    short_name = data.get('short_name', '')
    user_status = data.get('studentStatus', {}).get('name', 'Noma’lum')

    # Django User yaratish
    django_user, created = User.objects.get_or_create(
        username=hemis_id,
        defaults={'first_name': short_name}
    )
    if created:
        django_user.set_unusable_password()
        django_user.save()

    # UserHemis modelini yangilash
    user_hemis, _ = UserHemis.objects.get_or_create(
        hemis_id=hemis_id,
        defaults={
            'phone': phone,
            'short_name': short_name,
            'userStatus': user_status,
            'user': django_user,
        }
    )

    # Bog'lanmagan bo‘lsa, bog‘lash
    if not user_hemis.user:
        user_hemis.user = django_user
        user_hemis.save()

    # Login
    django_login(request, django_user)

    return redirect('student')

def logout(request):
    django_logout(request)
    request.session.flush()
    return redirect('home')

@login_required
def get_user(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'user': 'Token topilmadi'})

    response = requests.get(settings.HEMIS_OATUHT2_API_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })

    if response.status_code != 200:
        return JsonResponse({'user': 'Xatolik'})

    user_info = response.json().get('data', {})
    return user_info

@login_required
def student(request):
    users = get_user(request)
    context = {
        'users': users,
    }   
    return render(request, 'interaktiv/student.html', context)

@login_required
def profile(request):
    users = get_user(request)
    timestamp = users['birth_date']
    users['birth_date'] = datetime.fromtimestamp(timestamp)
    context = {
        'users': users,
    }
    return render(request, 'interaktiv/profile.html', context)

@login_required
def location(request):
    users = get_user(request)
    context = {
        'users': users,
    }
    return render(request, 'interaktiv/location.html', context)

@login_required
def education(request):
    users = get_user(request)
    context = {
        'users': users,
    }
    return render(request, 'interaktiv/education.html', context)

@login_required
def user_application(request):
    users = get_user(request)
    if users['level']['name'] == '1-kurs':
        if request.method == 'POST':
            new_phone = request.POST.get('new_phone')
            file = request.FILES.get('file')

            if not new_phone or not file:
                messages.error(request, "Barcha maydonlarni to‘ldiring.")
                return redirect('student')

            GrantApplication.objects.create(
                user=request.user,
                new_phone=new_phone,
                file=file,
                faculty=users['faculty']['name'] if users.get('faculty') else '',
                group=users['group']['name'] if users.get('group') else '',
                gpa_ball=users['avg_gpa'] if users.get('avg_gpa') else 0.0,
                
            )

            messages.success(request, "Arizangiz muvaffaqiyatli yuborildi!")
            return redirect('student')  # yoki boshqa sahifaga
    else:
        messages.error(request, "Faqat 1-kurs talabalar ariza yuborishi mumkin.")
        return redirect('student')

    context = {
        'users': users,
    }
    return render(request, 'interaktiv/user_application.html', context)

@login_required
def grant_application_list(request):
    users = get_user(request)
    applications = GrantApplication.objects.filter(user=request.user).order_by('-application_date')
    context = {
        'users': users,
        'applications': applications,
    }
    return render(request, 'interaktiv/grant_application_list.html',context)


@login_required
def admins(request):
    applications = GrantApplication.objects.all().order_by('-id')
    context = {
        'users': applications,
    }   
    return render(request, 'interaktiv/admins.html', context)

@login_required
def application_detail(request, hemis_id):
    try:
        application = GrantApplication.objects.get(user=hemis_id)
        user = get_user_info(hemis_id)
    except GrantApplication.DoesNotExist:
        messages.error(request, "Ariza topilmadi.")
        return redirect('admins')

    if request.method == 'POST':
        status = request.POST.get('status')
        comments = request.POST.get('comments', '')

        if status in ['approved', 'rejected']:
            application.status = status
            application.comments = comments
            application.save()
            messages.success(request, "Ariza holati yangilandi.")
            return redirect('admins')

    context = {
        'application': application,
        'user': user,
    }
    return render(request, 'interaktiv/application_detail.html', context)