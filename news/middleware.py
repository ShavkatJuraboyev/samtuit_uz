
# import os
# import uuid

# def get_mac_address(ip):
#     try:
#         mac = os.popen(f"arp -n {ip}").read().split()
#         return mac[3] if len(mac) > 3 else "Unknown"
#     except:
#         return "Unknown"

# class CaptureIPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         ip = request.META.get('HTTP_X_FORWARDED_FOR')
#         if ip:
#             ip = ip.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')

#         user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

#         # MAC-manzil olish (faqat mahalliy tarmoq ichida ishlaydi)
#         mac_address = get_mac_address(ip) if ip.startswith("172.20.") else "N/A"

#         request.user_ip = ip
#         request.user_agent = user_agent
#         request.user_mac = mac_address

#         response = self.get_response(request)
#         return response

class CaptureIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        print(f"IP: {ip}, User-Agent: {user_agent}")  # Debug maqsadida

        # Request obyektiga IP va User-Agent qo‘shish
        request.user_ip = ip
        request.user_agent = user_agent

        response = self.get_response(request)
        
        return response
