from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in [reverse('login'), reverse('signup')]:
            return None

        token = request.COOKIES.get('auth_token')
        if not token:
            return redirect('login')

        return None
