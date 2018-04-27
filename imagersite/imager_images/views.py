from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Album, Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def album_view(request, album_id=None):
    





    return render(request, 'imager_images/album.html', context)


def photo_view(request, photo_id=None):
    





    return render(request, 'imager_images/photo.html', context)


def library_view(request):
    """View for library."""
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(user__username=username)
    photos = Photo.objects.filter(album__user__username=username)

    context = {
        'profile': profile,
        'albums': [{'cover': album.cover, 'link': reverse('album', args=[album.id])} for album in albums],
        'photos': [{'thumb': photo, 'link': reverse('photo', args=[photo.id])} for photo in photos]
    }





    return render(request, 'imager_images/library.html', context)