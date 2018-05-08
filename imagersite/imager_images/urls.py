from django.urls import path
from .views import LibraryView, PhotoView, AlbumView


urlpatterns = [
    path('library', LibraryView.as_view(), name='library'),
    path('photos/<str:photo_id>', PhotoView.as_view(), name='photo'),
    path('photos', PhotoView.as_view(), name='photos'),
    path('albums', AlbumView.as_view(), name='albums'),
    path('albums/<str:album_id>', AlbumView.as_view(), name='album'),
]
