import nested_admin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self) -> None:
        super().clean()
        correct_count = 0
        for form in self.forms:
            if self.can_delete and form.cleaned_data.get("DELETE", False):
                continue
            if not form.cleaned_data:
                continue
            if form.cleaned_data.get("is_correct", False):
                correct_count += 1

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
    formset = AnswerInlineFormSet


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    fields = ("text", "has_one_correct_answer", "duplicate_button")
    readonly_fields = ("duplicate_button",)
    inlines = [AnswerInline]

    def duplicate_button(self, obj: Question) -> str:
        """Кнопка дублирования вопроса"""
        if obj.pk:
            return format_html(
                '<a class="button" href="{}">Дублировать</a>',
                reverse("admin:duplicate-question", args=[obj.pk]),
            )
        return ""

    duplicate_button.short_description = "Дублировать вопрос"  # type: ignore


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title",)

    def get_urls(self):
        """Добавляем новый URL для дублирования вопроса"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "duplicate-question/<int:question_id>/",
                self.admin_site.admin_view(self.duplicate_question),
                name="duplicate-question",
            ),
        ]
        return custom_urls + urls

    def duplicate_question(self, request, question_id):
        """Создает дубликат вопроса"""
        question = get_object_or_404(Question, pk=question_id)
        test_id = question.test.pk  # Получаем ID теста

        new_question = Question.objects.create(
            text=f"{question.text} (копия)",
            test=question.test,
            has_one_correct_answer=question.has_one_correct_answer,
        )

        # Дублируем ответы
        for answer in question.answers.all():
            Answer.objects.create(
                text=answer.text,
                is_correct=answer.is_correct,
                question=new_question,
            )

        # Возвращаем пользователя обратно в тест, где был дублированный вопрос
        return redirect(
            reverse("admin:quizz_test_change", args=[test_id]),
        )
