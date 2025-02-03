from django.shortcuts import render

from django.contrib import messages  # Make sure to import messages

from .models import About

from .forms import CollaborateForm


def info(request):

    """

    Renders the About page

    """


    if request.method == "POST":

        collaborate_form = CollaborateForm(data=request.POST)

        if collaborate_form.is_valid():

            collaborate_form.save()

            messages.add_message(request, messages.SUCCESS, "Collaboration request received! I endeavour to respond within 2 working days.")


    about = About.objects.all().order_by('-updated_on').first()  # Fetch the latest About entry

    collaborate_form = CollaborateForm()


    return render(

        request,

        "info/info.html",

        {

            "about": about,  # Pass the 'about' object to the template

            "collaborate_form": collaborate_form

        },

    )