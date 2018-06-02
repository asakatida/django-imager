from django.urls import path

from .views import (AddAlbumView, AddPhotoView, AlbumsView, AlbumView,
                    EditAlbumView, EditPhotoView, LibraryView, PhotosView,
                    PhotoView)

urlpatterns = [
    path('albums', AlbumsView.as_view(), name='albums'),
    path('albums/add', AddAlbumView.as_view(), name='albums_add'),
    path('albums/<str:album_id>', AlbumView.as_view(), name='album'),
    path(
        'albums/<str:album_id>/edit',
        EditAlbumView.as_view(),
        name='albums_edit'),
    path('library', LibraryView.as_view(), name='library'),
    path('photos', PhotosView.as_view(), name='photos'),
    path('photos/add', AddPhotoView.as_view(), name='photos_add'),
    path('photos/<str:photo_id>', PhotoView.as_view(), name='photo'),
    path(
        'photos/<str:photo_id>/edit',
        EditPhotoView.as_view(),
        name='photos_edit'),
]
