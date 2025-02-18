import nested_admin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self) -> None:
        super().clean()
        non_deleted_forms = [
            form
            for form in self.forms
            if not (self.can_delete and form.cleaned_data.get("DELETE", False))
        ]
        if not non_deleted_forms:
            return

        correct_count = 0
        for form in non_deleted_forms:
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
                    "Если выбран режим нескольких правильных ответов, выберите"
                    " минимум два варианта, помеченных как правильные.",
                )


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0
    fields = ("text", "is_correct")
    formset = AnswerInlineFormSet


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 0
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
        return (
            "Нажмите кнопку *Сохранить и продолжить редактирование* "
            "чтобы дублировать"
        )

    duplicate_button.short_description = "Дублировать вопрос"  # type: ignore


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title",)

    def get_urls(self) -> list:
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

    def duplicate_question(
        self,
        request: HttpRequest,
        question_id: int,
    ) -> HttpResponse:
        """Создает дубликат вопроса"""
        question = get_object_or_404(Question, pk=question_id)
        test_id = question.test.pk

        new_question = Question.objects.create(
            text=f"{question.text} (копия)",
            test=question.test,
            has_one_correct_answer=question.has_one_correct_answer,
        )

        for answer in question.answers.all():
            Answer.objects.create(
                text=answer.text,
                is_correct=answer.is_correct,
                question=new_question,
            )

        return redirect(
            reverse("admin:quizz_test_change", args=[test_id]),
        )
