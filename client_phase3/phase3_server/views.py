from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import asyncio
import websockets
import json
from asgiref.sync import sync_to_async


async def send_to_websocket(data, uri="ws://localhost:1423"):
    """Send data to the WebSocket server."""
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(data)
            response = await websocket.recv()
            return json.loads(response)
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON response from server"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def async_wrapper(func, *args, **kwargs):
    return await sync_to_async(func)(*args, **kwargs)


async def test_view(request):
    response = await send_to_websocket("signin deno deno")
    return HttpResponse(response, content_type="text/plain")


async def home_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")

    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")

    data_string = f"{token} schedules"
    response = await send_to_websocket(data_string)

    action_result = await async_wrapper(request.session.pop, "action_result", None)
    action_request = await async_wrapper(request.session.pop, "action_request", None)

    events = []
    schedules = response.get("schedules", [])
    colors = ["#CC6666", "#000", "#6666FF", "#FFFF99", "red", "#FF99FF"]
    color_index = 0
    for schedule in schedules:
        color = colors[color_index]
        color_index = (color_index + 1) % len(colors)
        for event in schedule["events"]:
            print(color,event["description"])
            event = {
                "title": event["description"] + "(" + event["event_type"].lower()+ ")",
                "start": event["start_time"],
                "end": event["end_time"],
                "color": color,
            }
            events.append(event)

    context = {
        "schedule_names": [schedule["description"] for schedule in schedules],
        "events": events,
        "action_result": action_result,
        "action_request": action_request,
        "authorized": request.session.get("username", None),
        "page": "home"
    }

    return await async_wrapper(render, request, "home.html", context)

async def user_views(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")

    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")

    data_string = f"{token} views"
    response = await send_to_websocket(data_string)

    action_result = await async_wrapper(request.session.pop, "action_result", None)
    action_request = await async_wrapper(request.session.pop, "action_request", None)

    events = []
    views = response.get("views", [])
    schedules = []
    if len(views) != 0:

        schedules = views[0].get("schedules", [])
        print(schedules)
        colors = ["#CC6666", "#000", "#6666FF", "#FFFF99", "red", "#FF99FF"]
        color_index = 0
        for schedule in schedules:
            color = colors[color_index]
            color_index = (color_index + 1) % len(colors)
            print("EVENTS:", schedule["events"])
            for event in schedule["events"]:
                event = {
                    "title": event[5] + "(" + event[6].lower()+ ")",
                    "start": event[2],
                    "end": event[3],
                    "color": color,
                }
                events.append(event)


    context = {
        "schedule_names": [schedule["description"] for schedule in schedules],
        "events": events,
        "action_result": action_result,
        "action_request": action_request,
        "authorized": request.session.get("username", None),
        "page": "views",
        "view_name": response.get("description", None)
    }
    print(context["events"])

    return await async_wrapper(render, request, "home.html", context)





async def signup_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")
    if token:
        messages.success(request, "Your session has not expired yet.")
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        fullname_quoted = f"'{fullname}'" if " " in fullname else fullname
        data_string = f"adduser {username} {email} {fullname_quoted} {password}"
        response = await send_to_websocket(data_string)

        if response["status"] == "success":
            messages.success(request, "Signup successful. Please log in.")
        else:
            messages.error(request, "Signup failed. Please try again.")
        return redirect("login")
    return render(request, "login_signup.html")


async def login_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")
    if token:
        messages.success(request, "Your session has not expired yet.")
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        data_string = f"signin {username} {password}"
        response = await send_to_websocket(data_string)

        if response["status"] == "success":
            await async_wrapper(request.session.__setitem__, "username", username)
            token = response["token"]
            expiration = response["expiration"]
            messages.success(request, f"Welcome {username}!")
            redirect_response = HttpResponseRedirect(reverse("home"))
            redirect_response.set_cookie(
                "auth_token", token, max_age=expiration, httponly=True
            )
            return redirect_response
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login_signup.html")


async def logout_view(request):
    await async_wrapper(request.session.flush)
    response = HttpResponseRedirect(reverse("login"))
    response.delete_cookie("auth_token")
    return response


async def add_schedule_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")
    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")

    if request.method == "POST":
        description = request.POST["description"]
        protection = request.POST["protection"]
        data_string = f"{token} addschedule {description} {protection}"
        response = await send_to_websocket(data_string)

        if response["status"] == "success":
            pass
        else:
            messages.error(request, f"Failed to add schedule. {response['message']}")
    if request.META.get("HTTP_REFERER") and "user_views" in request.META.get("HTTP_REFERER"):
        return redirect("user_views")
    else:
        return redirect("home")


async def add_event_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")
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

        data_string = (
            f"{token} addevent {schedule_name} {event_type} "
            f"{start} {end} {period} {description} {location} "
            f"{protection} {assignee}"
        )
        response = await send_to_websocket(data_string)

        if response["status"] == "error":
            messages.error(request, f"Failed to add event. {response['message']}")
        else:
            messages.success(request, "Event added successfully.")
    if request.META.get("HTTP_REFERER") and "user_views" in request.META.get("HTTP_REFERER"):
        return redirect("user_views")
    else:
        return redirect("home")

async def delete_event_view(request):
    token = await async_wrapper(request.COOKIES.get, "auth_token")
    if not token:
        messages.error(request, "Authentication required.")
        return redirect("login")

    if request.method == "POST":
        schedule_name = request.POST["schedule_name"]
        description = request.POST["event_name"]

        data_string = (
            f"{token} deleteevent {schedule_name} {description} "
        )
        response = await send_to_websocket(data_string)

        if response["status"] == "error":
            messages.error(request, f"Failed to delete event. {response['message']}")
        else:
            messages.success(request, "Event deleted successfully.")
    if request.META.get("HTTP_REFERER") and "user_views" in request.META.get("HTTP_REFERER"):
        return redirect("user_views")
    else:
        return redirect("home")


async def other_action_view(request):
    if request.method == "POST":
        token = await async_wrapper(request.COOKIES.get, "auth_token")
        if not token:
            messages.error(request, "Authentication required.")
            return redirect("login")

        action = request.POST["action"]
        data_string = f"{token} {action}"
        response = await send_to_websocket(data_string)

        await async_wrapper(request.session.__setitem__, "action_result", response)
        await async_wrapper(request.session.__setitem__, "action_request", action)
    if request.META.get("HTTP_REFERER") and "user_views" in request.META.get("HTTP_REFERER"):
        return redirect("user_views")
    else:
        return redirect("home")
