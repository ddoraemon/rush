from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import json
import socket
import fcntl
import struct

def index(request):
    local_ip = get_ip_address("eth0")
    return render_to_response("index.html", locals())
    
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
