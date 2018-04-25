from django.test import TestCase
from .models import ImagerProfile, User
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """ make factory """
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


class ProfileFactory(factory.django.DjangoModelFactory):
    """ setup factory """
    class Meta:
        model = ImagerProfile

    bio = factory.Faker('paragraphs')
    phone = factory.Faker('phone_number')
    locatiion = factory.Faker('geo_coordinate')
    website = factory.Faker('url')
    fee = factory.Faker('pydecimal', right_digits=2, positive=True)
    camera = factory.Faker(
        'random_element',
        elements=[
            ('DSLR', 'Digital Single Lens Reflex'),
            ('M', "Mirrorless"),
            ('AC', 'Advanced Compact'),
            ('SLR', 'Single Lens Reflex')])

    services = factory.Faker(
        'random_element',
        elements=[
            ('weddings', 'Weddings'),
            ('headshots', 'HeadShots'),
            ('landscape', 'LandScape'),
            ('portraits', 'Portraits'),
            ('art', 'Art')])

    photostyles = factory.Faker(
        'random_element',
        elements=[
            ('blackandwhite', 'Black and White'),
            ('night', 'Night'),
            ('macro', 'Macro'),
            ('3d', '3D'),
            ('artistic',     'Artistic'),
            ('underwater', 'Underwater')])


class ProfileUnitTests(TestCase):
    """ profile tests"""
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            profile = ProfileFactory.create(user=user)
            profile.save()

    @classmethod
    def tearDownClass(cls):
        """ tear down class """
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_its_profile(self):
        """ test user profile view """
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)
