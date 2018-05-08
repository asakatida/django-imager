from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Album, Photo
from .models import ImagerProfile
from random import sample
from django.views.generic import TemplateView


class ProfileView(TemplateView):
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
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]

        return context

    def get(self, request, *args, username=None, **kwargs):
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

