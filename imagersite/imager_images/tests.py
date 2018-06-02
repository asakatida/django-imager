"""Test."""

from tempfile import NamedTemporaryFile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from factory import Faker
from factory.django import DjangoModelFactory
from model_mommy import mommy

from .forms import AlbumForm, PhotoForm
from .models import Album, Photo


class PhotoFactory(DjangoModelFactory):
    """Make photo factory."""

    class Meta:
        """Class for Meta."""

        model = Photo

    image = Faker('image_url')
    description = Faker('word')
    date_uploaded = Faker('date')
    date_modified = Faker('date')
    date_published = Faker('date')
    published = Faker(
        'random_element',
        elements=[
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
        ]
    )


class AlbumFactory(DjangoModelFactory):
    """Make photo factory."""

    class Meta:
        """Class for Meta."""

        model = Album
    description = Faker('text', max_nb_chars=250, ext_word_list=None)
    date_created = Faker('date')
    date_modified = Faker('date')
    date_published = Faker('date')
    published = Faker(
        'random_element',
        elements=[
            ('PRIVATE', 'Private'),
            ('SHARED', 'Shared'),
            ('PUBLIC', 'Public'),
        ]
    )


class ProfileUnitTests(TestCase):
    """Profile tests."""

    user = None
    image = None

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


class ImageTests(TestCase):
    """Testing Routes."""

    @classmethod
    def setUpClass(cls):
        """Define class."""
        super().setUpClass()

        for _ in range(10):
            user = mommy.make(User)
            user.set_password('password')
            user.save()
            album = mommy.make(Album, user=user)
            photo = mommy.make(
                Photo,
                image=NamedTemporaryFile(suffix='.jpg').name)
            album.photos.add(photo)

    @classmethod
    def tearDownClass(cls):
        """Tear Down Class."""
        User.objects.all().delete()
        super().tearDownClass()


class ImageViewTests(ImageTests):
    """
    Image view tests.
    """

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
        response = self.client.get(
            reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertEqual(response.status_code, 200)

    def test_user_photo_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(
            reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_photo(self):
        """Test id user can see other user view."""
        response = self.client.get(
            reverse_lazy('photo', args=[Photo.objects.first().id]))
        self.assertEqual(response.status_code, 302)

    def test_user_can_see_photos(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('photos'))
        self.assertEqual(response.status_code, 200)

    def test_user_photos_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('photos'))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_photos(self):
        """Test id user can see other user view."""
        response = self.client.get(reverse_lazy('photos'))
        self.assertEqual(response.status_code, 302)

    def test_user_can_see_library(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('library'))
        self.assertEqual(response.status_code, 200)

    def test_user_library_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('library'))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_library(self):
        """Test id user can see other user view."""
        response = self.client.get(reverse_lazy('library'))
        self.assertEqual(response.status_code, 302)

    def test_user_can_see_album_one(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(
            reverse_lazy('album', args=[Album.objects.first().id]))
        self.assertEqual(response.status_code, 200)

    def test_user_album_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(
            reverse_lazy('album', args=[Album.objects.first().id]))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_album(self):
        """Test id user can see other user view."""
        response = self.client.get(
            reverse_lazy('album', args=[Album.objects.first().id]))
        self.assertEqual(response.status_code, 302)

    def test_user_can_see_albums(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('albums'))
        self.assertEqual(response.status_code, 200)

    def test_user_albums_view_uses_base_template(self):
        """Test id user can see other user view."""
        users = list(User.objects.all())
        self.client.force_login(users[0])
        response = self.client.get(reverse_lazy('albums'))
        self.assertTemplateUsed(response, 'generic/base.html')

    def test_user_must_be_logged_in_to_see_albums(self):
        """Test id user can see other user view."""
        response = self.client.get(reverse_lazy('albums'))
        self.assertEqual(response.status_code, 302)


class ImageFormTests(ImageTests):
    """Image form tests class."""

    @classmethod
    def setUpClass(cls):
        """Define class."""
        super().setUpClass()

        cls.user = mommy.make(User)
        cls.user.set_password('password')
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        """Tear Down Class."""
        User.objects.all().delete()
        super().tearDownClass()

    def test_init_album(self):
        """Test image form."""
        AlbumForm(username=self.user.username)

    def test_init_photo(self):
        """Test image form."""
        PhotoForm(username=self.user.username)

    def test_valid_data_album(self):
        """Test image form."""
        user = list(User.objects.all())[0]
        form = AlbumForm(
            {
                'description': '',
                'cover': Photo.objects.first(),
                'title': 'Title',
                'published': Photo.objects.first().published,
                'photos': []},
            username=user.username)
        form.cover = Photo.objects.first()
        form.photos = [Photo.objects.first()]
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_data_album(self):
        """Test image form."""
        user = list(User.objects.all())[0]
        form = AlbumForm({}, username=user.username)
        self.assertFalse(form.is_valid())

    def test_invalid_data_photo(self):
        """Test image form."""
        user = list(User.objects.all())[0]
        form = PhotoForm({}, username=user.username)
        self.assertFalse(form.is_valid())
