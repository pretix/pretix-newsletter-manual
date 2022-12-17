from django.urls import path

from .views import ManualSettings

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/newsletter_manual/settings",
        ManualSettings.as_view(),
        name="settings",
    )
]
