import pytz
from django.utils.translation import gettext as _, gettext_lazy
from pretix.base.exporter import ListExporter
from pretix.base.settings import PERSON_NAME_SCHEMES
from pretix.base.models.orders import InvoiceAddress

from .models import NewsletterRequest


class RequestListExporter(ListExporter):
    identifier = "newsletter_manual_requestlist"
    verbose_name = gettext_lazy("Newsletter subscription requests")

    def iterate_list(self, form_data):
        qs = (
            NewsletterRequest.objects.filter(order__event__in=self.events)
            .order_by("created")
            .prefetch_related("order", "order__all_positions")
        )

        headers = [_("Order code"), _("Email"), _("Request date"), _("Name")]

        has_name_parts = False
        if self.event:
            name_scheme = PERSON_NAME_SCHEMES[self.event.settings.name_scheme]
            has_name_parts = len(name_scheme["fields"]) > 1
            if has_name_parts:
                for k, label, w in name_scheme["fields"]:
                    headers.append(label)
        yield headers

        for r in qs.select_related("order", "order__event"):
            tz = pytz.timezone(r.order.event.settings.timezone)
            op_with_attendee_name = next(
                (
                    op
                    for op in r.order.all_positions.all()
                    if not op.canceled and op.attendee_name
                ),
                None,
            )

            row = [
                r.order.code,
                r.order.email,
                r.created.astimezone(tz).strftime("%Y-%m-%d"),
            ]
            try:
                if r.order.invoice_address and r.order.invoice_address.name:
                    row += [r.order.invoice_address.name]
                    if has_name_parts:
                        for k, label, w in name_scheme["fields"]:
                            row.append(r.order.invoice_address.name_parts.get(k, ""))
                elif op_with_attendee_name:
                    row += [op_with_attendee_name.attendee_name]
                    if has_name_parts:
                        for k, label, w in name_scheme["fields"]:
                            row.append(op_with_attendee_name.attendee_name_parts.get(k, ""))
                else:
                    row += [""] * (
                        1 + (len(name_scheme["fields"]) if has_name_parts else 0)
                    )
            except InvoiceAddress.DoesNotExist:
                if op_with_attendee_name:
                    row += [op_with_attendee_name.attendee_name]
                    if has_name_parts:
                        for k, label, w in name_scheme["fields"]:
                            row.append(op_with_attendee_name.attendee_name_parts.get(k, ""))
                else:
                    row += [""] * (
                        1 + (len(name_scheme["fields"]) if has_name_parts else 0)
                    )


            yield row
