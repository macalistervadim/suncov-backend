from django.db import models
from django.utils.translation import gettext_lazy as _


class Theme(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=30,
        unique=True,
        null=False,
    )

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Theme")

    def __str__(self) -> str:
        return f"{self.title}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r})"


class PartOfSpeech(models.Model):
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        related_name="theme",
        verbose_name=_("theme"),
    )
    text = models.TextField(
        verbose_name=_("text"),
    )

    class Meta:
        verbose_name = _("Partofspeech")
        verbose_name_plural = _("Partofspeechs")

    def __str__(self) -> str:
        return f"{self.theme} - {self.text[:50]}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"theme={self.theme!r}, "
            f"text={self.text!r})"
        )
