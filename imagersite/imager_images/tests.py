"""Test."""
from django.test import TestCase
from .models import Photo, Album
import factory
from django.contrib.auth import get_user_model
import faker
from django.contrib.auth.models import User

fake = faker.Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Make photo factory."""

    class Meta:
        """Meat Pie."""

        model = Photo

    image = factory.Faker('image_url')
    description = factory.Faker('word')
    date_uploaded = factory.Faker('date')
    date_modified = factory.Faker('date')
    date_published = factory.Faker('date')
    published = factory.Faker(
        'random_element',
        elements=[
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
         ]
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Make photo factory."""

    class Meta:
        """Meat Pie."""

        model = Album
    description = fake.text(max_nb_chars=250, ext_word_list=None)
    date_created = factory.Faker('date')
    date_modified = factory.Faker('date')
    date_published = factory.Faker('date')
    published = factory.Faker(
        'random_element',
        elements=[
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
         ]
    )


class ProfileUnitTests(TestCase):
    """Profile tests."""

    def test_user_can_see_its_profile(self):
        """Test user profile view."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.set_password('potatoe')
        user.save()
        self.user = user
        image = PhotoFactory.build()
        image.user = self.user
        image.save()
        self.image = image
