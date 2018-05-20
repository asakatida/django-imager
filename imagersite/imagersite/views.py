"""
Base app views.
"""

from random import sample

from django.views.generic import TemplateView

from imagersite.imager_images.models import Photo


class HomeView(TemplateView):
    """
    Home view class.
    """

    template_name = 'generic/home.html'

    def get_context_data(self, *args, **kwargs):
        """
        Home view.
        """
        context = super().get_context_data(**kwargs)
        photos = list(Photo.objects.filter(published="PUBLIC"))
        if photos:
            context['background'] = sample(photos, 1)[0]

        return context
