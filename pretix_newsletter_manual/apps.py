from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_newsletter_manual"
    verbose_name = "Newsletter address collection (manual)"

    class PretixPluginMeta:
        name = gettext_lazy("Newsletter address collection (manual)")
        author = "pretix team"
        description = gettext_lazy("Manually collect newsletter registrations")
        visible = True
        version = __version__
        category = "INTEGRATION"
        compatibility = "pretix>=3.0.0"

    def ready(self):
        from . import signals  # NOQA


