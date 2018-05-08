from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Album, Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from random import sample
from django.views.generic import TemplateView, CreateView, DetailView


class MixIn:
    """Mix In class."""

    @staticmethod
    def _public_or_user(model, username):
        if model == Photo:
            return model.objects.filter(Q(album__user__username=username) | Q(published="PUBLIC"))
        return model.objects.filter(Q(user__username=username) | Q(published="PUBLIC"))

    @staticmethod
    def _album_with_cover(photos, cover):
        if cover is not None:
            return set(photos) | {cover}
        return photos

    def get_context_data(self, *args, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]
        # if self.photo_id:
        #     photo = get_object_or_404(Photo, id=self.photo_id)
        #     context['photo'] = photo
        #     self.template_name = 'imager_images/photo.html'

        return context


class UserNameMixIn:
    """Mixin class."""

    def get(self, request, *args, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')
        username = request.user.get_username()
        if username == '':
            return redirect('home')
        self.username = username
        return super().get(request, *args, **kwargs)


class AlbumView(UserNameMixIn, MixIn, DetailView):
    """Class for Album view."""

    template_name = 'imager_images/album.html'
    pk_url_kwarg = 'album_id'
    model = Album

    def get_content_data(self, *args, **kwargs):
        """Album view."""
        context = super().get_context_data(**kwargs)
        context['photos'] = self._album_with_cover(context['photos'].filter(album__id=context['album'].id), context['album'].cover)
        context['cover'] = context['album'].cover or sample(list(context['photos']) + [None], 1)[0]
        return context


class AlbumsView(UserNameMixIn, MixIn, TemplateView):
    """Class for Albums view."""

    template_name = 'imager_images/albums.html'


class PhotoView(UserNameMixIn, MixIn, DetailView):
    """Class for Photo view."""

    template_name = 'imager_images/photo.html'
    pk_url_kwarg = 'photo_id'
    model = Photo


class PhotosView(UserNameMixIn, MixIn, TemplateView):
    """Class for Photos view."""

    template_name = 'imager_images/photos.html'


class LibraryView(UserNameMixIn, MixIn, TemplateView):
    """Class for Library view."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, *args, **kwargs):
        """View for library."""
        context = super().get_context_data(**kwargs)
        albums = Album.objects.filter(user__username=self.username)
        photos = Photo.objects.filter(album__user__username=self.username)

        context['albums'] = albums
        context['photos'] = photos
        return context


class AddPhotoView(CreateView):
    """Class for Photo view."""

    model = Photo
    template_name = 'imager_images/add_photo.html'
    success_url = 'library'

    def get(self, *args, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Post method."""
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        """Get form method."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        """From validation."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddAlbumView(CreateView):
    """Class for Album view."""

    model = Album
    template_name = 'imager_images/add_album.html'
    success_url = 'library'

    def get(self, *args, **kwargs):
        """Get method."""
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Post method."""
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        """Get form method."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        """Form validation."""
        form.instance.user = self.request.user
        return super().form_valid(form)
