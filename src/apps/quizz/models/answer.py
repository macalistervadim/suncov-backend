from django.db import models
from django.utils.translation import gettext_lazy as _


class Answer(models.Model):
    text = models.CharField(verbose_name=_("text"), max_length=200)
    is_correct = models.BooleanField(
        verbose_name=_("is_correct"), default=False,
    )
    question = models.ForeignKey(
        "Question",
        related_name="answers",
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
    )

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self) -> str:
        return f"{self.text!r}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(question={self.question!r}, "
            f"text={self.text!r}, "
            f"is_correct={self.is_correct!r})"
        )
