from django.shortcuts import render



def album_view(request, album_id=None):
    





    return render(request, 'imager_images/album.html', context)


def photo_view(request, photo_id=None):
    





    return render(request, 'imager_images/photo.html', context)


def library_view(request):
    





    return render(request, 'imager_images/library.html', context)