from django.conf.urls import url
from webapp.views import UserRegistration, UserAutorization

urlpatterns = [
    url(r'^registration$', UserRegistration.as_view(),
        name="user_registration"),
    url(r'^authorization$', UserAutorization.as_view(),
        name="user_authorization"),
]
