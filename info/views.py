from django.shortcuts import render
from django.contrib import messages
from .forms import CollaborateForm


def info(request):
    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(request, messages.SUCCESS, "Received.")

    collaborate_form = CollaborateForm()

    return render(
        request,
        "info/info.html",
        {
            "collaborate_form": collaborate_form
        },
    )
