from random import sample
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileEditForm
from django.urls import reverse_lazy


class ProfileView(TemplateView):
    """Class for Profile view."""

    template_name = 'imager_profile/profile.html'

    def get_context_data(self, *args, **kwargs):
        """View for user profile."""
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(ImagerProfile, user__username=self.username)
        albums = Album.objects.filter(user__username=self.username)
        photos = Photo.objects.filter(album__user__username=self.username)

        if not self.owner:
            photos = Photo.objects.filter(published='PUBLIC')
            albums = Album.objects.filter(published='PUBLIC')

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        if photos:
            context['background'] = sample(photos, 1)[0]

        return context

    def get(self, request, *args, username=None, **kwargs):
        """Get function."""
        if not self.request.user.is_authenticated:
            return redirect('home')
        self.owner = False

        if not username:
            username = request.user.get_username()
            self.owner = True
            if username == '':
                return redirect('home')
        else:
            username = request.user.get_username()
            if not username:
                return redirect('home')
        self.username = username
        return super().get(request, *args, username=username, **kwargs)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Profile Edit Veiw."""

    template_name = 'imager_profile/profile.html'
    model = ImagerProfile
    form_class = ProfileEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, *args, **kwargs):
        """Get method."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Post method."""
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        """Get from arg."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.get_username()})
        return kwargs

    def form_valid(self, form):
        """From validation."""
        form.instance.user.email = form.data['email']
        form.instance.user.first_name = form.data['first_name']
        form.instance.user.last_name = form.data['last_name']
        form.instance.user.save()
        return super().form_valid(form)
