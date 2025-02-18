from django.db import models
from django.utils.translation import gettext_lazy as _


class Test(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=200)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r})"
        )
