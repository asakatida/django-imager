from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from .forms import AlbumForm, PhotoForm, EditAlbumForm, EditPhotoForm


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


class AlbumView(UserNameMixIn, DetailView):
    """Class for Album view."""

    template_name = 'imager_images/album.html'
    pk_url_kwarg = 'album_id'
    model = Album

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

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]
        context['photos'] = self._album_with_cover(context['photos'].filter(album__id=context['album'].id), context['album'].cover)
        context['cover'] = context['album'].cover or sample(list(context['photos']) + [None], 1)[0]

        return context


class AlbumsView(UserNameMixIn, ListView):
    """Class for Albums view."""

    template_name = 'imager_images/albums.html'
    model = Album

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

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]

        return context


class PhotoView(UserNameMixIn, DetailView):
    """Class for Photo view."""

    template_name = 'imager_images/photo.html'
    pk_url_kwarg = 'photo_id'
    model = 'Photo'


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

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]

        return context


class PhotosView(UserNameMixIn, ListView):
    """Class for Photos view."""

    template_name = 'imager_images/photos.html'
    model = Photo

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

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]

        return context


class LibraryView(UserNameMixIn, ListView):
    """Class for Library view."""

    template_name = 'imager_images/library.html'
    model = Album

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

    def get_context_data(self, **kwargs):
        """Photo View."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(User, username=self.username)
        albums = (self._public_or_user(Album, self.username))
        photos = (self._public_or_user(Photo, self.username))

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]
        albums = Album.objects.filter(user__username=self.username)
        photos = Photo.objects.filter(album__user__username=self.username)

        context['album_add'] = reverse('albums_add')
        context['photo_add'] = reverse('photos_add')
        context['albums'] = albums
        context['photos'] = photos
        return context


class AddPhotoView(CreateView):
    """Class for Photo view."""

    form_class = PhotoForm
    model = 'Photo'
    template_name = 'imager_images/add_photo.html'
    pk_url_kwarg = 'photo_id'
    success_url = reverse_lazy('library')

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

    def get_queryset(self):
        return self.model.objects.filter(album__user__username=self.request.user.get_username())


class AddAlbumView(CreateView):
    """Class for Album view."""

    form_class = AlbumForm
    model = 'Album'
    template_name = 'imager_images/add_album.html'
    pk_url_kwarg = 'album_id'
    success_url = reverse_lazy('library')

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

    def get_queryset(self):
        return self.model.objects.filter(user__username=self.request.user.get_username())


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

    def form_valid(self, form):
        """Validate form."""
        return super().form_valid(form)

    def get_queryset(self):
        """Get Query set."""
        return self.model.objects.filter(user__username=self.request.user.get_username())


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

    def get(self, *args, **kwargs):
        """Get."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Post."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        """Get."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.get_username()})
        return kwargs

    def form_valid(self, form):
        """Validate form."""
        return super().form_valid(form)

    def get_queryset(self):
        """Get Q set."""
        return self.model.objects.filter(album__user__username=self.request.user.get_username())
