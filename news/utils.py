# utils.py

import subprocess
import re

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')

def get_mac_address(ip_address):
    try:
        output = subprocess.check_output(['arp', '-a', ip_address], stderr=subprocess.DEVNULL).decode()
        mac = re.search(r'(([a-fA-F0-9]{2}[:-]){5}[a-fA-F0-9]{2})', output)
        if mac:
            return mac.group(0)
    except Exception:
        return None
    return None
