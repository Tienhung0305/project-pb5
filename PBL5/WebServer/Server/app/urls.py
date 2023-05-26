from django.urls import path
from app import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False
        ),
    ),
    path('/start_in',views.start_in),
    path('/start_out',views.start_out)
]


