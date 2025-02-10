from django.db import models


class Answer(models.Model):
    question = models.ForeignKey(
        "Question",
        related_name="answers",
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(question={self.question!r}, "
            f"text={self.text!r}, "
            f"is_correct={self.is_correct!r})"
        )
