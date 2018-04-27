from django.urls import path
from .views import library_view, photo_view, album_view


urlpatterns = [
    path('library', library_view, name='library'),
    path('photos/<str:photo_id>', photo_view, name='photo'),
    path('photos', photo_view, name='photos'),
    path('albums', album_view, name='albums'),
    path('albums/<str:album_id>', album_view, name='album'),
]
