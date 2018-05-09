from django.urls import path
from .views import LibraryView, PhotoView, AlbumView, AddPhotoView, AddAlbumView, AlbumsView, PhotosView


urlpatterns = [
    path('photos/add', AddPhotoView.as_view(), name='photos_add'),
    path('albums/add', AddAlbumView.as_view(), name='albums_add'),
    path('library', LibraryView.as_view(), name='library'),
    path('photos/<str:photo_id>', PhotoView.as_view(), name='photo'),
    path('photos', PhotosView.as_view(), name='photos'),
    path('albums', AlbumsView.as_view(), name='albums'),
    path('albums/<str:album_id>', AlbumView.as_view(), name='album'),
    
]
