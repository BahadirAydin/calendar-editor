from django.http import HttpResponse
from django.shortcuts import render
from .tcp_connection_manager import TCPConnectionManager
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

tcp_manager = TCPConnectionManager()

def connect_view(request):
    tcp_manager.connect('localhost', 1423)
    if tcp_manager.client_socket:
        url = reverse('login')
        return redirect(url)
    else:
        return HttpResponse("<h1>Could not establish connection. Make sure TCP server is up and running</h1>")
    
def test_view(request):
    if tcp_manager.client_socket:
        tcp_manager.send("adduser")
        response = tcp_manager.receive()
        return HttpResponse(response, content_type="text/plain")
    else:
        return HttpResponse("sdsdf", content_type="text/plain")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # Redirect to a success page.
        # else:
        #     return render(request, 'login_signup.html', {'error': 'Invalid credentials'})
    return render(request, 'login_signup.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        # User.objects.create_user(username=username, password=password)
        return redirect('login')  # Redirect to the login page after signup.
    return render(request, 'login_signup.html')
