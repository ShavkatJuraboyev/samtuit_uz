class CaptureIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Foydalanuvchi haqiqiy IP-manzilini olish
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]  # Bir nechta IP-manzillar bo'lsa, birinchisini olish
        else:
            ip = request.META.get('REMOTE_ADDR')  # Agar HTTP_X_FORWARDED_FOR bo'lmasa, REMOTE_ADDR'dan foydalanish

        request.user_ip = ip  # So'rovga IP-manzilni qo'shish
        response = self.get_response(request)
        return response
