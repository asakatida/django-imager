from imager_images.models import Photo
from .serializers import PhotoSerializer
from rest_framework import generics


class PhotosList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Photo.objects.filter(album__user=self.request.user)
    serializer_class = PhotoSerializer
