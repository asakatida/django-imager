from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Album, Photo
from .models import ImagerProfile
from random import sample


def profile_view(request, username=None):
    """View for user profile."""
    owner = False

    if not username:
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')
    else:
        if not request.user.get_username():
            return redirect('home')

    profile = get_object_or_404(ImagerProfile, user__username=username)
    albums = Album.objects.filter(user__username=username)
    photos = Photo.objects.filter(album__user__username=username)

    if not owner:
        photos = Photo.objects.filter(published='PUBLIC')
        albums = Album.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
        'background': sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
    }

    return render(request, 'imager_profile/profile.html', context)
