import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from interaktiv.models import UserHemis, GrantApplication
from django.contrib.auth.decorators import login_required 
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import openpyxl
from django.http import HttpResponse


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

    # Ariza topshirish muddati (masalan, 2024-06-10 gacha)
    deadline = datetime(2025, 8, 10)
    if datetime.now() > deadline:
        messages.error(request, "Ariza topshirish muddati tugadi.")
        return redirect('student')

    if users['level']['name'] == '1-kurs':
        # Foydalanuvchining arizasi mavjudmi va statusi "Kutulmoqda"mi tekshiramiz
        existing_application = GrantApplication.objects.filter(
            user=request.user
        ).first()

        if existing_application:
            messages.error(request, "Siz avval ariza yuborgansiz.")
            return redirect('student')


        if request.method == 'POST':
            new_phone = request.POST.get('new_phone')
            file = request.FILES.get('file')
            social_activism_field = request.FILES.get('social_activism_field')

            # GPA tekshiruvi
            gpa = users.get('avg_gpa', 0.0)
            try:
                gpa = float(gpa)
            except (TypeError, ValueError):
                gpa = 0.0

            if gpa < 3.5:
                messages.error(request, "Ariza topshirish uchun GPA 3.5 yoki undan yuqori bo‘lishi kerak.")
                return redirect('student')

            if not new_phone or not file:
                messages.error(request, "Barcha maydonlarni to‘ldiring.")
                return redirect('student')

            GrantApplication.objects.create(
                user=request.user,
                new_phone=new_phone,
                file=file,
                social_activism_field=social_activism_field,
                faculty=users['faculty']['name'] if users.get('faculty') else '',
                group=users['group']['name'] if users.get('group') else '',
                gpa_ball=gpa,
            )

            messages.success(request, "Arizangiz muvaffaqiyatli yuborildi!")
            return redirect('student')
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
def update_grant_file(request, pk):
    application = get_object_or_404(GrantApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        file = request.FILES.get('file')
        social_activism_field = request.FILES.get('social_activism_field')

        # Ariza fayli yangilansa, eski faylni o‘chirish va yangisini qo‘yish
        if file:
            if application.file:
                application.file.delete(save=False)  # Faylni diskdan o‘chirish
            application.file = file

        # Ijtimoiy faoliyat fayli yangilansa, eski faylni o‘chirish va yangisini qo‘yish
        if social_activism_field:
            if application.social_activism_field:
                application.social_activism_field.delete(save=False)
            application.social_activism_field = social_activism_field

        application.save()
        messages.success(request, "Fayllar muvaffaqiyatli yangilandi.")
        return redirect('grant_application_list')

    return redirect('grant_application_list')


@login_required
def admins(request):
    faculty = request.GET.get('faculty')
    gpa = request.GET.get('gpa')
    name = request.GET.get('name')
    per_page = request.GET.get('per_page', 20)

    applications = GrantApplication.objects.all().order_by('-id')

    if faculty:
        applications = applications.filter(faculty__icontains=faculty)

    if gpa:
        try:
            gpa_value = float(gpa)
            applications = applications.filter(gpa_ball__gte=gpa_value)
        except ValueError:
            pass  # noto‘g‘ri GPA kiritilsa, filterlash o‘tmaydi
    if name:
        applications = applications.filter(user__first_name__icontains=name)  # yoki `icontains=user__full_name` agar mavjud bo‘lsa

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 20

    paginator = Paginator(applications, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    per_page_choices = [10, 20, 50, 100] 

    context = {
        'users': page_obj,
        'faculty_filter': faculty or '',
        'gpa_filter': gpa or '',
        'name_filter': name or '',
        'per_page': per_page,
        'total_count': applications.count(),
        'per_page_choices': per_page_choices,
    }
    return render(request, 'interaktiv/admins.html', context)

@login_required
def application_detail(request, application_id):
    try:
        application = GrantApplication.objects.get(id=application_id)
        hemis_id = application.user.userhemis.hemis_id  # UserHemis orqali hemis_id
        user_info = get_user_info(hemis_id)  # HEMIS API dan ma'lumot
        if user_info.get('success'):
            user_data = user_info['data']
        else:
            user_data = None
    except GrantApplication.DoesNotExist:
        messages.error(request, "Ariza topilmadi.")
        return redirect('admins')
    except AttributeError:
        messages.error(request, "Foydalanuvchining HEMIS IDsi topilmadi.")
        return redirect('admins')

    if request.method == 'POST':
        status = request.POST.get('status')
        comments = request.POST.get('comments', '')
        ball = request.POST.get('ball')
        show_scores = request.POST.get('show_scores') == 'on'

        if status in ['approved', 'rejected']:
            try:
                application.ball = float(ball)
            except (TypeError, ValueError):
                application.ball = None
            application.status = status
            application.comments = comments
            
            application.is_visible_to_user = show_scores
            application.save()
            messages.success(request, "Ariza holati yangilandi.")
            return redirect('admins')

    context = {
        'application': application,
        'user': user_data,  # faqat data bo'limini templatega yuboramiz
    }
    return render(request, 'interaktiv/application_detail.html', context)

@login_required
def export_applications_excel(request):
    faculty = request.GET.get('faculty')
    gpa = request.GET.get('gpa')

    applications = GrantApplication.objects.all().order_by('-id')

    if faculty:
        applications = applications.filter(faculty__icontains=faculty)

    if gpa:
        try:
            gpa_value = float(gpa)
            applications = applications.filter(gpa_ball__gte=gpa_value)
        except ValueError:
            pass

    # Excel fayl yaratish
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Grant arizalari"

    # Sarlavhalar
    ws.append(['#', 'Foydalanuvchi ismi', 'Fakultet', 'Guruh', 'GPA', 'Holati', 'Tel'])

    # Ma'lumotlarni to'ldirish
    for idx, app in enumerate(applications, 1):
        ws.append([
            idx,
            app.user.first_name,   # username o‘rniga first_name
            app.faculty,
            app.group,
            app.gpa_ball,
            app.get_status_display(),
            app.new_phone
        ])

    # Javobni tayyorlash
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=grant_arizalari.xlsx'
    wb.save(response)
    return response