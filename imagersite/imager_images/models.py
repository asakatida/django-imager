"""Models."""
from random import sample

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from sorl.thumbnail import ImageField


class Photo(models.Model):
    """Photo."""

    image = ImageField(upload_to='images')
    title = models.CharField(max_length=250, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=250,
        choices=(
            ('PRIVATE', 'Private'),
            ('PUBLIC', 'Public')))

    @classmethod
    def public_or_user(cls, username):
        """
        Public or user.
        """
        return cls.objects.filter(
            models.Q(album__user__username=username)
            | models.Q(published="PUBLIC"))


class Album(models.Model):
    """Album."""

    user = models.ForeignKey(
        User, related_name='album', on_delete=models.CASCADE, null=False)
    photos = models.ManyToManyField(Photo, related_name='album')
    title = models.CharField(max_length=250, default='Untitled')
    description = models.TextField(blank=True, null=True)
    cover = models.ForeignKey(
        Photo, on_delete=models.SET_NULL, related_name='+', null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    hidden = models.BooleanField(default=False)
    published = models.CharField(
        max_length=250,
        choices=(
            ('PRIVATE', 'Private'),
            ('PUBLIC', 'Public')))

    def get_cover(self):
        """Get the signed cover or random."""
        return self.cover or sample(list(self.photos_set) + [None], 1)[0]

    @classmethod
    def public_or_user(cls, username):
        """
        Public or user.
        """
        return cls.objects.filter(
            models.Q(user__username=username) | models.Q(published="PUBLIC"))

    def with_cover(self):
        """
        All photos with cover.
        """
        if self.cover is not None:
            return set(self.photos) | {self.cover}
        return self.photos


@receiver(models.signals.post_save, sender=User)
def create_hidden_album(sender, *args, created=False, instance=None, **kwargs):
    """Create Base Album with kwargs."""
    if created:
        album = Album(user=instance, hidden=True)
        album.save()


@receiver(models.signals.post_save, sender=Photo)
def create_profile(sender, *args, created=False, instance=None, **kwargs):
    """Add to Base Album with kwargs."""
    if created:
        instance.album_set.append(Album.objects.filter(hidden=True).first())
