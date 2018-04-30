from django.test import TestCase
from .models import ImagerProfile, User
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Make factory."""

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


def populate_profile(user, **kwargs):
    """Populate profile."""
    user.profile.bio = kwargs['bio'] if 'bio' in kwargs else factory.Faker('paragraphs')
    user.profile.phone = kwargs['phone'] if 'phone' in kwargs else factory.Faker('phone_number')
    user.profile.locatiion = kwargs['locatiion'] if 'locatiion' in kwargs else factory.Faker('geo_coordinate')
    user.profile.website = kwargs['website'] if 'website' in kwargs else factory.Faker('url')
    user.profile.fee = kwargs['fee'] if 'fee' in kwargs else factory.Faker('pydecimal', right_digits=2, positive=True)
    user.profile.camera = kwargs['camera'] if 'camera' in kwargs else factory.Faker(
        'random_element',
        elements=[
            ('DSLR', 'Digital Single Lens Reflex'),
            ('M', "Mirrorless"),
            ('AC', 'Advanced Compact'),
            ('SLR', 'Single Lens Reflex')])

    user.profile.services = kwargs['services'] if 'services' in kwargs else factory.Faker(
        'random_element',
        elements=[
            ('weddings', 'Weddings'),
            ('headshots', 'HeadShots'),
            ('landscape', 'LandScape'),
            ('portraits', 'Portraits'),
            ('art', 'Art')])

    user.profile.photostyles = kwargs['photostyles'] if 'photostyles' in kwargs else factory.Faker(
        'random_element',
        elements=[
            ('blackandwhite', 'Black and White'),
            ('night', 'Night'),
            ('macro', 'Macro'),
            ('3d', '3D'),
            ('artistic',     'Artistic'),
            ('underwater', 'Underwater')])


class ProfileUnitTests(TestCase):
    """Profile tests."""

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()
            populate_profile(user)

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_its_profile(self):
        """Test user profile view."""
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)
