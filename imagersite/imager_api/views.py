from rest_framework import generics

from imager_images.models import Photo

from .serializers import PhotoSerializer


class PhotosList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Photo.objects.filter(album__user=self.request.user)
    serializer_class = PhotoSerializer
