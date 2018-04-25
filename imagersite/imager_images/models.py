"""Models."""
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Photo(models.Model):
    """Go away."""

    image = ImageField(upload_to='images')
    title = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=7,
        choices=(
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
        )
    )

    def __str__(self):
        """Str magic."""
        return '{}'.format(self.title)


class Album(models.Model):
    """Album."""

    user = models.OneToOneField(User, related_name='album', on_delete=models.CASCADE, null=False)
    photos = models.ManyToManyField(Photo, related_name='photos')
    title = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=7,
        choices=(
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
        )
    )

    def __str__(self):
        """Str."""
        return '{}'.format(self.title)
