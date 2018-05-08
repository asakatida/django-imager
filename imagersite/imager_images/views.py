from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Album, Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from random import sample
from django.views.generic import TemplateView


def _public_or_user(model, username):
    if model == Photo:
        return model.objects.filter(Q(album__user__username=username) | Q(published="PUBLIC"))
    return model.objects.filter(Q(user__username=username) | Q(published="PUBLIC"))


def _album_with_cover(photos, cover):
    if cover is not None:
        return set(photos) | {cover}
    return photos


class AlbumView(TemplateView):
    template_name = 'imager_images/albums.html'

    def get_context_data(self, *args, **kwargs):
        """Album View."""

        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (_public_or_user(Album, self.username))
        photos = (_public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
        
        if self.album_id:
            # import pdb; pdb.set_trace()
            album = get_object_or_404(Album, id=self.album_id)
            # import pdb; pdb.set_trace()
            context["photos"] = _album_with_cover(_public_or_user(Photo, self.username).filter(album__id=self.album_id), album.cover)
            context["album"] = album
            context["cover"] = album.cover or sample(list(context['photos']) + [None], 1)[0]
            self.template_name = 'imager_images/album.html'
        return context

    def get(self, request, *args, album_id=None, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')
        self.owner = False
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')
        self.username = username
        self.album_id = album_id
        return super().get(request, *args, album_id=album_id, **kwargs)


class PhotoView(TemplateView):
    template_name = 'imager_images/photos.html'

    def get_context_data(self, *args, **kwargs):
        """Photo View."""

        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (_public_or_user(Album, self.username))
        photos = (_public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
        if self.photo_id:
            photo = get_object_or_404(Photo, id=self.photo_id)
            context['photo'] = photo
            self.template_name = 'imager_images/photo.html'

        return context

    def get(self, request, *args, photo_id=None, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')
        self.owner = False
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')
        self.username = username
        self.photo_id = photo_id
        return super().get(request, *args, photo_id=photo_id, **kwargs)

class LibraryView(TemplateView):
    template_name = 'imager_images/library.html'
    
    def get_context_data(self, *args, **kwargs):
        """View for library."""
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.username)
        albums = Album.objects.filter(user__username=self.username)
        photos = Photo.objects.filter(album__user__username=self.username)

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]

        return context

    def get(self, request, *args, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')
        self.owner = False
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')
        self.username = username
        return super().get(request, *args, **kwargs)
