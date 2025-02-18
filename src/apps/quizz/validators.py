from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet


class AnswerInlineFormSet(BaseInlineFormSet):
    """Форма для проверки корректных ответов"""

    def clean(self) -> None:
        super().clean()
        non_deleted_forms = [
            form
            for form in self.forms
            if not (self.can_delete and form.cleaned_data.get("DELETE", False))
        ]
        if not non_deleted_forms:
            return

        correct_count = sum(
            1
            for form in non_deleted_forms
            if form.cleaned_data.get("is_correct", False)
        )

        if self.instance.has_one_correct_answer:
            if correct_count != 1:
                raise ValidationError(
                    "Если выбран режим одного правильного ответа, "
                    "выберите ровно один вариант, помеченный как правильный.",
                )
        else:
            if correct_count < 2:
                raise ValidationError(
                    "Если выбран режим нескольких правильных ответов, выберите"
                    " минимум два варианта, помеченных как правильные.",
                )
