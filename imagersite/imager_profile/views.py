from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Album, Photo
from .models import ImagerProfile


def profile_view(request, username=None):
    """View for user profile."""
    owner = False

    if not username:
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')

    profile = get_object_or_404(ImagerProfile, user__username=username)
    albums = Album.objects.filter(user__username=username)
    photos = Photo.objects.filter(product__user__username=username)

    if not owner:
        photos = Photo.objects.filter(published='PUBLIC')
        albums = Album.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos
    }

    return render(request, 'imager_profile/profile.html', context)
