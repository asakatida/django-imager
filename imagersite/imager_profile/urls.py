from django.urls import path
from .views import ProfileView, ProfileEditView


urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('edit', ProfileEditView.as_view(), name='settings'),
    path('<str:username>', ProfileView.as_view(), name='named_profile'),
]
