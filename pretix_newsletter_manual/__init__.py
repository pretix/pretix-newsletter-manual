from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
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


default_app_config = "pretix_newsletter_manual.PluginApp"
