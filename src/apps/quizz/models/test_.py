from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r})"
