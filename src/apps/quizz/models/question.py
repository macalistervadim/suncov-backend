from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    text = models.CharField(verbose_name=_("text"), max_length=500)
    test = models.ForeignKey(
        "Test",
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name=_("test"),
    )
    has_one_correct_answer = models.BooleanField(
        default=True,
        verbose_name=_("has_one_correct_answer"),
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"test={self.test!r}, "
            f"text={self.text!r}, "
            f"has_one_correct_answer={self.has_one_correct_answer!r})"
        )
