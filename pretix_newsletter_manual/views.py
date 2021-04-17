import logging
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from i18nfield.forms import I18nFormField, I18nTextInput
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin

logger = logging.getLogger(__name__)


class NewsletterSettingsForm(SettingsForm):
    newsletter_manual_text = I18nFormField(
        label=_("Checkbox label"),
        required=True,
        widget=I18nTextInput,
    )


class ManualSettings(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = NewsletterSettingsForm
    template_name = "pretix_newsletter_manual/settings.html"
    permission = "can_change_event_settings"

    def get_success_url(self) -> str:
        return reverse(
            "plugins:pretix_newsletter_manual:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
