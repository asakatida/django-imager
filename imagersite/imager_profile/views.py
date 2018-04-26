from django.shortcuts import render

def profile_view(request, username=None):






    return render(request, 'imager_profile/profile.html', context)


def album_view(request, album_id=None):
    





    return render(request, 'imager_profile/album.html', context)


def photo_view(request, photo_id=None):
    





    return render(request, 'imager_profile/photo.html', context)


def library_view(request):
    





    return render(request, 'imager_profile/library.html', context)