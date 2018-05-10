from .models import ShopperProfile
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, widgets


class ProfileEditForm(ModelForm):
    """Profile Edit."""

    email = CharField(
        max_length=User._meta.get_field('email').max_length,
        widget=widgets.EmailInput())

    first_name = CharField(
        max_length=User._meta.get_field('first_name').max_length,
        required=False)

    last_name = CharField(
        max_length=User._meta.get_field('last_name').max_length,
        required=False)

    class Meta:
        model = ShopperProfile
        fields = ['first_name', 'last_name', 'email', 'street', 'city', 'state', 'zip_code', 'cell', 'home']

    def __init__(self, *args, **kwargs):
        """Init."""
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = User.objects.get(username=username).email
        self.fields['first_name'].initial = User.objects.get(username=username).first_name
        self.fields['last_name'].initial = User.objects.get(username=username).last_name
        self.fields['street'].initial = ShopperProfile.objects.get(user__username=username).street