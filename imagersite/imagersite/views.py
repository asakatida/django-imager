from django.shortcuts import render
from imager_images.models import Photo
from random import sample
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home view class."""

    template_name = 'generic/home.html'

    def get_context_data(self, *args, **kwargs):
        """Home view."""
        context = super().get_context_data(**kwargs)
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]

        return context
