from django.shortcuts import render
from imager_images.models import Photo
from random import sample


def home_view(request):
    """Home view."""
    context = {
        "background": sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
    }
    return render(request, 'generic/home.html', context)


