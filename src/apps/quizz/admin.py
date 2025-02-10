import nested_admin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = 0
        for form in self.forms:
            # Если форма пуста или помечена на удаление – пропускаем
            if self.can_delete and form.cleaned_data.get("DELETE", False):
                continue
            if not form.cleaned_data:
                continue
            if form.cleaned_data.get("is_correct", False):
                correct_count += 1

        # Получаем значение режима из родительского вопроса
        # (self.instance – это объект Question, к которому привязаны ответы)
        if self.instance.has_one_correct_answer:
            if correct_count != 1:
                raise ValidationError(
                    "Если выбран режим одного правильного ответа, "
                    "выберите ровно один вариант, помеченный как правильный.",
                )
        else:
            if correct_count < 2:
                raise ValidationError(
                    "Если выбран режим нескольких правильных ответов, "
                    "выберите минимум два варианта, помеченных как правильные",
                )


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 1
    fields = ("text", "is_correct")
    formset = AnswerInlineFormSet  # используем наш кастомный formset


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    fields = ("text", "has_one_correct_answer")
    inlines = [AnswerInline]


class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
