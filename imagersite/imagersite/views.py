from django.shortcuts import render


def home_view(request):
    """ home view """"
    return render(request, 'generic/home.html', {})
