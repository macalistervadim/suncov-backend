from django.db import models


class Question(models.Model):
    test = models.ForeignKey(
        "Test",
        related_name="questions",
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=500)
    has_one_correct_answer = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(test={self.test!r}, "
            f"text={self.text!r}, "
            f"has_one_correct_answer={self.has_one_correct_answer!r})"
        )
