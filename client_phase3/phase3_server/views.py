from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .tcp_connection_manager import TCPConnectionManager
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

tcp_manager = TCPConnectionManager()


def connect_view(request):
    tcp_manager.connect("localhost", 1423)
    if tcp_manager.is_connected():
        url = reverse("login")
        return redirect(url)
    else:
        return HttpResponse(
            "<h1>Could not establish connection. Make sure TCP server is up and running</h1>"
        )


def test_view(request):
    if tcp_manager.client_socket:
        tcp_manager.send("adduser")
        response = tcp_manager.receive()
        return HttpResponse(response, content_type="text/plain")
    else:
        return HttpResponse("sdsdf", content_type="text/plain")


def home_view(request):
    token = request.COOKIES.get('auth_token')
    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")
    tcp_manager.send("{} homeview".format(token))
    response = tcp_manager.receive()
    response = eval(response)
    if response["status"] == "error":
        return render(request, "home.html", {"schedules": []})
    return render(request, "home.html", {"schedules": response["schedules"]})

def signup_view(request):
    if not tcp_manager.is_connected():
        url = reverse("login")
        return redirect(url)

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        if (len(fullname.split(" "))) > 1:
            fullname = "'" + fullname + "'"
        tcp_manager.send(
            "adduser {} {} {} {}".format(username, email, fullname, password)
        )
        response = tcp_manager.receive()
        response = eval(response)
        if response["status"] == "success":
            messages.success(request, "Signup successful. Please log in.")
        else:
            messages.error(request, "Signup failed. Please try again.")
        return redirect("login")
    return render(request, "login_signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        tcp_manager.send("signin {} {}".format(username, password))
        response = tcp_manager.receive()
        print(response)
        response = eval(response)
        if response["status"] == "success":
            request.session["username"] = username
            token = response["token"] 
            expiration = response["expiration"]
            messages.success(request, "Welcome {}!".format(username))
            redirect_response = HttpResponseRedirect(reverse("home"))
            redirect_response.set_cookie('auth_token', token, max_age=expiration, httponly=True)
            return redirect_response
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login_signup.html")

def logout_view(request):
    request.session.flush()
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('auth_token')
    return response

def add_schedule_view(request):
    token = request.COOKIES.get('auth_token')
    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")
    
    if request.method == "POST":
        description = request.POST["description"]
        protection = request.POST["protection"]
        tcp_manager.send("{} addschedule {} {} ".format(token, description, protection))
        response = tcp_manager.receive()
        response = eval(response)
        if response["status"] == "success":
            return redirect("home")
        else:
            messages.error(request, f"Failed to add schedule. {response['message']}")
            return redirect("home")
    return redirect("home")


def add_event_view(request):
    token = request.COOKIES.get('auth_token')
    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")

    if request.method == "POST":
        schedule_name = request.POST["schedule_name"]
        event_type = request.POST["event_type"]
        start = request.POST["start_time"]
        end = request.POST["end_time"]
        period = request.POST["period"]
        description = request.POST["description"]
        location = request.POST["location"]
        protection = request.POST["protection"]
        assignee = request.POST["assignee"]

        tcp_manager.send(
            "{} addevent {} {} {} {} {} {} {} {} {}".format(
                token,
                schedule_name,
                event_type,
                start,
                end,
                period,
                description,
                location,
                protection,
                assignee,
            )
        )
        response = tcp_manager.receive()
        response = eval(response)
        if response["status"] == "error":
            messages.error(request, f"Failed to add event. {response['message']}")
        else:
            messages.success(request, "Event added successfully.")
            return redirect("home")
    return redirect("home")


