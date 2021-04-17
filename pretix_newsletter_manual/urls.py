from django.conf.urls import url

from .views import ManualSettings

urlpatterns = [
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/newsletter_manual/settings$",
        ManualSettings.as_view(),
        name="settings",
    ),
]
