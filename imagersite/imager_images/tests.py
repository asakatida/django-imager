"""Test."""
from django.test import TestCase
from .models import Photo, Album
import factory
from django.contrib.auth import get_user_model
import faker
from django.contrib.auth.models import User
from model_mommy import mommy
import tempfile
from django.urls import reverse_lazy


fake = faker.Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Make photo factory."""

    class Meta:
        """Class for Meta."""

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
        """Class for Meta."""

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


class TestStoreRoutes(TestCase):
    """Testing Routes."""

    @classmethod
    def setUpClass(cls):
        """Define class."""
        super().setUpClass()

        for n in range(10):
            user = mommy.make(User)
            user.set_password('password')
            user.save()
            album = mommy.make(Album, user=user)
            photo = mommy.make(
                Photo,
                image=tempfile.NamedTemporaryFile(suffix='.jpg').name)
            album.photos.add(photo)

    @classmethod
    def tearDownClass(cls):
        """Tear Down Class."""
        User.objects.all().delete()
        super().tearDownClass()

    def test_200_status_on_authenticated_request_to_store(self):
        """Test 200 status."""
        user = User.objects.first()
        # self.client.login(username=user.username, password='password')
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("albums"))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_200_status_on_authenticated_request_to_product(self):
        """Test authenticated 200 status."""
        user = User.objects.first()
        album = Album.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_302_status_on_unauthenticated_request_to_product(self):
        """Test 302 on unathenticated."""
        album = Album.objects.first()
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.assertEqual(response.status_code, 302)

    def test_404_status_on_bad_request_to_product(self):
        """Test 404 status on bad request."""
        response = self.client.get('/store/products/does_not_exist')
        self.assertEqual(response.status_code, 404)

    def test_302_status_on_unauthenticated_request_to_store(self):
        """Test 302 on not athenticated request to store."""
        response = self.client.get(reverse_lazy("albums"))
        self.assertEqual(response.status_code, 302)

    def test_only_public_products_are_shown(self):
        """Test that only public products shown."""
        user = User.objects.first()
        album = Album.objects.first()
        album.published = 'PUBLIC'
        album.save()

        self.client.force_login(user)
        response = self.client.get(reverse_lazy("albums"))
        self.client.logout()

        albums = response.context['albums']
        for album in albums:
            self.assertEqual(album.published, 'PUBLIC')

    def test_user_can_see_photo_one(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertEqual(response.status_code, 200)

    def test_user_photo_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_photo(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        response = self.client.get(reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertEqual(response.status_code, 302)
