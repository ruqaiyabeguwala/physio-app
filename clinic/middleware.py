from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class SimpleLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse("simple_login")
        if request.path.startswith("/static/") or request.path == login_url:
            return self.get_response(request)

        if request.session.get("simple_logged_in"):
            return self.get_response(request)

        next_url = request.get_full_path()
        return redirect(f"{login_url}?next={next_url}")

