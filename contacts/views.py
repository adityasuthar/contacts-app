from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.db.models import Q

# Create your views here.


def contact_list(request):
    query = request.GET.get("q")
    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
    else:
        contacts = Contact.objects.all()
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/contact_detail.html", {"contact": contact})


def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect("contact_detail", pk=contact.pk)  # why pk?
    else:
        form = ContactForm()
    return render(request, "contacts/contact_edit.html", {"form": form})


def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            return redirect("contact_detail", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_edit.html", {"form": form})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    # Handle POST request for deletion
    if request.method == "POST":
        contact.delete()
        return redirect("contact_list")  # Redirect to contact list after deletion

    # Render delete confirmation page for GET request
    return render(request, "contacts/contact_confirm_delete.html", {"contact": contact})
