from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
from django.dispatch import receiver


class ImagerProfile(models.Model):
    """Main Class."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    locatiion = models.CharField(max_length=180, blank=True, null=True)
    website = models.URLField(max_length=180, blank=True, null=True)
    fee = models.FloatField(blank=True, null=True)
    camera = models.CharField(max_length=180, blank=True, null=True,
                              choices=(('DSLR', 'Digital Single Lens Reflex'),
                                       ('M', "Mirrorless"),
                                       ('AC', 'Advanced Compact'),
                                       ('SLR', 'Single Lens Reflex')))

    services = MultiSelectField(
        choices=(('weddings', 'Weddings'),
                 ('headshots', 'HeadShots'),
                 ('landscape', 'LandScape'),
                 ('portraits', 'Portraits'),
                 ('art', 'Art')))

    photostyles = MultiSelectField(
        choices=(('blackandwhite', 'Black and White'),
                 ('night', 'Night'),
                 ('macro', 'Macro'),
                 ('3d', '3D'),
                 ('artistic', 'Artistic'),
                 ('underwater', 'Underwater')))

    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Str magic."""
        return self.user.username

    @classmethod
    def active(cls):
        """Class Active."""
        return cls.objects.filter(is_active=True)


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create Profile with kwargs."""
    if kwargs['created']:
        profile = ImagerProfile(user=kwargs['instance'])
        profile.save()
