from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AlbumForm, EditAlbumForm, EditPhotoForm, PhotoForm
from .models import Album, Photo


class AlbumView(LoginRequiredMixin, DetailView):
    """Class for Album view."""

    template_name = 'imager_images/album.html'
    pk_url_kwarg = 'album_id'
    model = Album

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(User, username=self.username)

        album = context['album']

        photos = album.with_cover()

        if photos:
            context['background'] = sample(photos, 1)[0]

        context['photos'] = photos
        context['cover'] = album.cover or sample(list(photos) + [None], 1)[0]

        return context


class AlbumsView(LoginRequiredMixin, ListView):
    """Class for Albums view."""

    template_name = 'imager_images/albums.html'
    model = Album

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(User, username=self.username)

        context['albums'] = Album.public_or_user(self.username)

        photos = Photo.public_or_user(self.username)

        if photos:
            context['background'] = sample(photos, 1)[0]

        context['photos'] = photos

        return context


class PhotoView(LoginRequiredMixin, DetailView):
    """Class for Photo view."""

    template_name = 'imager_images/photo.html'
    pk_url_kwarg = 'photo_id'
    model = 'Photo'

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(User, username=self.username)

        context['albums'] = Album.public_or_user(self.username)

        photos = Photo.public_or_user(self.username)

        if photos:
            context['background'] = sample(photos, 1)[0]

        context['photos'] = photos

        return context


class PhotosView(LoginRequiredMixin, ListView):
    """Class for Photos view."""

    template_name = 'imager_images/photos.html'
    model = Photo

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(User, username=self.username)

        context['albums'] = Album.public_or_user(self.username)

        photos = Photo.public_or_user(self.username)

        if photos:
            context['background'] = sample(photos, 1)[0]

        context['photos'] = photos

        return context


class LibraryView(LoginRequiredMixin, ListView):
    """Class for Library view."""

    template_name = 'imager_images/library.html'
    model = Album

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(User, username=self.username)

        photos = Photo.public_or_user(self.username)

        if photos:
            context['background'] = sample(photos, 1)[0]

        context['albums'] = Album.objects.filter(user__username=self.username)
        context['photos'] = Photo.objects.filter(
            album__user__username=self.username)

        return context


class AddPhotoView(LoginRequiredMixin, CreateView):
    """Class for Photo view."""

    form_class = PhotoForm
    model = 'Photo'
    template_name = 'imager_images/add_photo.html'
    pk_url_kwarg = 'photo_id'
    success_url = reverse_lazy('library')

    def get_form_kwargs(self):
        """Get form method."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        """From validation."""
        Album.objects.filter(
            user=self.request.user, hidden=True
        ).first().photos.add(
            self.instance)
        return super().form_valid(form)

    def get_queryset(self):
        """
        Get queryset.
        """
        return self.model.objects.filter(
            album__user__username=self.request.user.get_username())


class AddAlbumView(LoginRequiredMixin, CreateView):
    """Class for Album view."""

    form_class = AlbumForm
    model = 'Album'
    template_name = 'imager_images/add_album.html'
    pk_url_kwarg = 'album_id'
    success_url = reverse_lazy('library')

    def get_form_kwargs(self):
        """Get form method."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        """Form validation."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        """
        Get queryset.
        """
        return self.model.objects.filter(
            user__username=self.request.user.get_username())


class EditAlbumView(LoginRequiredMixin, UpdateView):
    """Edit album view."""

    template_name = 'imager_images/edit_album.html'
    model = Album
    form_class = EditAlbumForm
    pk_url_kwarg = 'album_id'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')
    slug_url_kwarg = 'album_id'
    slug_field = 'id'

    def get(self, *args, **kwargs):
        """Define get."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Define post."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.get_username()})
        return kwargs

    def get_queryset(self):
        """Get Query set."""
        return self.model.objects.filter(
            user__username=self.request.user.get_username())


class EditPhotoView(LoginRequiredMixin, UpdateView):
    """Edit class."""

    template_name = 'imager_images/edit_photo.html'
    model = Photo
    form_class = EditPhotoForm
    pk_url_kwarg = 'photo_id'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')
    slug_url_kwarg = 'photo_id'
    slug_field = 'id'

    def get(self, *args, username=None, **kwargs):
        """Get."""
        return super().get(
            *args, username=self.request.user.get_username(), **kwargs)

    def post(self, *args, username=None, **kwargs):
        """Post."""
        return super().post(
            *args, username=self.request.user.get_username(), **kwargs)

    def get_form_kwargs(self):
        """Get."""
        kwargs = super().get_form_kwargs()
        kwargs['username'] = self.request.user.get_username()
        return kwargs

    def get_queryset(self):
        """Get Q set."""
        return self.model.objects.filter(
            album__user__username=self.request.user.get_username())
