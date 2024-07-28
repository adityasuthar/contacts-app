from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/", CustomLogoutView.as_view(), name="logout"
    ),  # Use the custom logout view
    path("register/", views.register, name="register"),
    path("", views.contact_list, name="contact_list"),
    path("contact/<int:pk>/", views.contact_detail, name="contact_detail"),
    path("contact/new/", views.contact_new, name="contact_new"),
    path("contact/<int:pk>/edit/", views.contact_edit, name="contact_edit"),
    path("contact/<int:pk>/delete/", views.contact_delete, name="contact_delete"),
    # path("accounts/", include("django.contrib.auth.urls")),
]
