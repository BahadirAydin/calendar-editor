from django.shortcuts import render

from django.http import HttpResponse
from .tcp_client import connect_to_tcp_server

def connect_view(request):
    connect_to_tcp_server('localhost', 1423)
    return render(request , "base.html")
