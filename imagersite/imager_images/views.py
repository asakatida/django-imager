from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Album, Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from random import sample


def _public_or_user(model, username):
    if model == Photo:
        return model.objects.filter(Q(album__user__username=username) | Q(published="PUBLIC"))
    return model.objects.filter(Q(user__username=username) | Q(published="PUBLIC"))


def _album_with_cover(photos, cover):
    if cover is not None:
        return set(photos) | {cover}
    return photos


def album_view(request, album_id=None):
    """Album View."""
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = (_public_or_user(Album, username))
    photos = (_public_or_user(Photo, username))

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
        'background': sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
    }
    if album_id:
        # import pdb; pdb.set_trace()
        album = get_object_or_404(Album, id=album_id)
        # import pdb; pdb.set_trace()
        context["photos"] = _album_with_cover(_public_or_user(Photo, username).filter(album__id=album.id), album.cover)
        context["album"] = album
        context["cover"] = album.cover or sample(list(context['photos']) + [None], 1)[0]
        return render(request, 'imager_images/album.html', context)
    return render(request, 'imager_images/albums.html', context)


def photo_view(request, photo_id=None):
    """Photo View."""
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)
        context = {
            'photo': photo,
            'background': sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
        }
        return render(request, 'imager_images/photo.html', context)
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = (_public_or_user(Album, username))
    photos = (_public_or_user(Photo, username))

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
        'background': sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
    }
    return render(request, 'imager_images/photos.html', context)


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
        'albums': albums,
        'photos': photos,
        'background': sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
    }
    return render(request, 'imager_images/library.html', context)
