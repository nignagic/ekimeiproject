from django.shortcuts import render


def ReactSpaLauncher(request):
    return render(request, "moviedatabase/spa/launcher.html")
