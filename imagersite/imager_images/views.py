from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Album, Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


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
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
    }
    if album_id:
        # import pdb; pdb.set_trace()
        album = get_object_or_404(Album, id=album_id)
        # import pdb; pdb.set_trace()
        print(album)
        context["photos"] = _album_with_cover(Photo.objects.filter(album__id=album.id).filter(published='PUBLIC'), album.cover)
        context["album"] = album
        return render(request, 'imager_images/album.html', context)
    return render(request, 'imager_images/albums.html', context)


def photo_view(request, photo_id=None):
    """Photo View."""
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)
        context = {
            'photo': {'thumb': photo, 'link': reverse('photo', args=[photo.id])}
        }
        return render(request, 'imager_images/photo.html', context)
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': [{'cover': album.cover, 'link': reverse('album',
                    args=[album.id])} for album in albums],
        'photos': [{'thumb': photo, 'link': reverse('photo', args=[photo.id])} for photo in photos]
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
        'albums': [{'cover': album.cover, 'link': reverse('album',
                    args=[album.id])} for album in albums],
        'photos': [{'thumb': photo, 'link': reverse('photo', args=[photo.id])} for photo in photos]
    }
    return render(request, 'imager_images/library.html', context)
