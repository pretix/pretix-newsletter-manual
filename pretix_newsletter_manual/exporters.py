import pytz
from django.utils.translation import gettext as _, gettext_lazy
from pretix.base.exporter import ListExporter
from pretix.base.models.orders import InvoiceAddress
from pretix.base.settings import PERSON_NAME_SCHEMES

from .models import NewsletterRequest


class RequestListExporter(ListExporter):
    identifier = "newsletter_manual_requestlist"
    verbose_name = gettext_lazy("Newsletter subscription requests")

    def iterate_list(self, form_data):
        qs = NewsletterRequest.objects.filter(order__event__in=self.events).order_by(
            "created"
        )

        headers = [
            _("Order code"),
            _("Email"),
            _("Request date"),
            _("Invoice Name"),
        ]

        if self.event:
            name_scheme = PERSON_NAME_SCHEMES[self.event.settings.name_scheme]
            if len(name_scheme["fields"]) > 1:
                for k, label, w in name_scheme["fields"]:
                    headers.append(label)
        yield headers

        for r in qs.select_related("order", "order__event"):
            tz = pytz.timezone(r.order.event.settings.timezone)

            row = [
                r.order.code,
                r.order.email,
                r.created.astimezone(tz).strftime("%Y-%m-%d"),
            ]

            try:
                row += [
                    r.order.invoice_address.name,
                ]
                if self.event and len(name_scheme["fields"]) > 1:
                    for k, label, w in name_scheme["fields"]:
                        row.append(r.order.invoice_address.name_parts.get(k, ""))
            except InvoiceAddress.DoesNotExist:
                row += [""] * (
                    1
                    + (
                        len(name_scheme["fields"])
                        if self.event and len(name_scheme["fields"]) > 1
                        else 0
                    )
                )
            yield row
