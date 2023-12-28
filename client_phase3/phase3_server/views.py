from django.http import HttpResponse
from django.shortcuts import render
from .tcp_connection_manager import TCPConnectionManager

tcp_manager = TCPConnectionManager()

def connect_view(request):
    tcp_manager.connect('localhost', 1423)
    return render(request, "base.html")

def test_view(request):
    if tcp_manager.client_socket:
        tcp_manager.send("adduser")
        response = tcp_manager.receive()
        return HttpResponse(response, content_type="text/plain")
    else:
        return HttpResponse("sdsdf", content_type="text/plain")

