from django.db import models
from django.utils.translation import gettext_lazy as _


class Theme(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=30,
        unique=True,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r})"


class Dictation(models.Model):
    theme = models.ForeignKey(
        Theme,
        verbose_name=_("theme"),
        related_name="dictations",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    text = models.TextField(verbose_name=_("text"))

    class Meta:
        verbose_name = _("Dictation")
        verbose_name_plural = _("Dictations")

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"theme={self.theme!r}, "
            f"title={self.title!r}, "
            f"text={self.text!r})"
        )
