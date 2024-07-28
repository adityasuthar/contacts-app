from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.views import View

# Create your views here.


@login_required
def contact_list(request):
    query = request.GET.get("q")
    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query),
        ).filter(user=request.user)
    else:
        contacts = Contact.objects.filter(user=request.user)
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    return render(request, "contacts/contact_detail.html", {"contact": contact})


@login_required
def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact = form.save()
            return redirect("contact_detail", pk=contact.pk)  # why pk?
    else:
        form = ContactForm()
    return render(request, "contacts/contact_edit.html", {"form": form})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            return redirect("contact_detail", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_edit.html", {"form": form})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    # Handle POST request for deletion
    if request.method == "POST":
        contact.delete()
        return redirect("contact_list")  # Redirect to contact list after deletion

    # Render delete confirmation page for GET request
    return render(request, "contacts/contact_confirm_delete.html", {"contact": contact})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("contact_list")
        else:
            return render(request, "registration/register.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})


class CustomLogoutView(View):
    # next_page = "login"  # Use the name of your login URL pattern

    def get(self, request, *args, **kwargs):
        print("get logout view")
        return redirect(reverse("login"))


# def logout_view(request):
#     logout(request)
#     return redirect("login")  # Redirect to login page after logout
