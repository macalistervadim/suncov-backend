from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PartofspeechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.partofspeech'
    verbose_name = _("Часть речи")
