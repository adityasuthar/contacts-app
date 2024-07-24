from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to access any view.
    If the user is not authenticated, they are redirected to the registration/login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require authentication
        exempt_urls = [
            reverse("login"),
            reverse("logout"),
            reverse("register"),
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect("register")

        response = self.get_response(request)
        return response
