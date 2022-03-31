from django import forms
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _, ugettext_noop
from i18nfield.strings import LazyI18nString
from pretix.base.settings import settings_hierarkey
from pretix.base.signals import (
    logentry_display,
    order_placed,
    register_data_exporters,
    register_multievent_data_exporters,
)
from pretix.base.templatetags.rich_text import rich_text_snippet
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import contact_form_fields

from pretix_newsletter_manual.exporters import RequestListExporter
from pretix_newsletter_manual.models import NewsletterRequest


@receiver(nav_event_settings, dispatch_uid="newsletter_manual_nav")
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_change_event_settings", request=request
    ):
        return []
    return [
        {
            "label": _("Newsletter"),
            "icon": "envelope-open",
            "url": reverse(
                "plugins:pretix_newsletter_manual:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_newsletter_manual",
        }
    ]


@receiver(order_placed, dispatch_uid="newsletter_manual_order_placed")
def order_placed(sender, order, **kwargs):
    if (
        order.meta_info_data.get("contact_form_data", {}).get("manual_newsletter")
        is True
        and order.email
    ):
        NewsletterRequest.objects.create(order=order)
        order.log_action("pretix_newsletter_manual.request")


@receiver(contact_form_fields, dispatch_uid="newsletter_manual_contact_form_fields")
def cf_formfields(sender, **kwargs):
    return {
        "manual_newsletter": forms.BooleanField(
            label=rich_text_snippet(sender.settings.newsletter_manual_text),
            required=False,
        )
    }


@receiver(signal=logentry_display, dispatch_uid="newsletter_manual_logentry_display")
def pretixcontrol_logentry_display(sender, logentry, **kwargs):
    if not logentry.action_type.startswith("pretix_newsletter_manual"):
        return

    plains = {
        "pretix_newsletter_manual.request": _(
            "A newsletter subscription has been requested."
        )
    }

    if logentry.action_type in plains:
        return plains[logentry.action_type]


@receiver(register_data_exporters, dispatch_uid="newsletter_manual_exporters")
def register_data_exporter(sender, **kwargs):
    return RequestListExporter


@receiver(
    register_multievent_data_exporters, dispatch_uid="newsletter_manual_exporters_multi"
)
def register_data_exporter_multi(sender, **kwargs):
    return RequestListExporter


settings_hierarkey.add_default(
    "newsletter_manual_text",
    LazyI18nString.from_gettext(
        ugettext_noop("Yes, I want to receive the organizer's newsletter")
    ),
    LazyI18nString,
)
