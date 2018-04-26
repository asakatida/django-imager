from django.urls import path
from .views import profile_view


urlpatterns = [
    path('', profile_view, name='profile'),
    path('<str:username>', profile_view, name='named_profile'),
    path('settings/<str:username>', profile_view, name='settings'),  # The view is not correct here. You need to define settings_view
    path('images/library', profile_view, name='library'),
    path('images/photos/<str:photo_id>', profile_view, name='photo'),
    path('images/photos', profile_view, name='photos'),
    path('images/albums', profile_view, name='albums'),
    path('images/albums/<str:album_id>', profile_view, name='album'),
]