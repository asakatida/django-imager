from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^photos/$', views.PhotosList.as_view()),
]
