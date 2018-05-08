"""Imports."""
from django.forms import ModelForm
from .models import Album, Photo


class AlbumForm(ModelForm):
    """Class for Album form."""

    class Meta:
        model = Album
        fields = ['cover', 'name', 'description', 'published']

    def __init__(self, *args, **kwargs):
        """Self init."""
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['cover'].queryset = Photo.objects.filter(product__user__username=username)