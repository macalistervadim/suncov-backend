import nested_admin
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test
from src.apps.quizz.validators import AnswerInlineFormSet


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
        if not obj.pk:
            return "Сохраните вопрос, чтобы его дублировать."

        url = reverse("admin:duplicate-question", args=[obj.pk])
        return format_html('<a class="button" href="{}">Дублировать</a>', url)

    duplicate_button.short_description = "Дублировать вопрос"  # type: ignore


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title",)

    def get_urls(self) -> list:
        """Добавляем новый URL для дублирования вопроса"""
        custom_urls = [
            path(
                "duplicate-question/<int:question_id>/",
                self.admin_site.admin_view(self.duplicate_question),
                name="duplicate-question",
            ),
        ]
        custom_urls.extend(super().get_urls())
        return custom_urls

    def duplicate_question(
        self,
        request: HttpRequest,
        question_id: int,
    ) -> HttpResponse:
        """Создает дубликат вопроса и его ответов"""
        question = get_object_or_404(Question, pk=question_id)

        new_question = Question.objects.create(
            text=f"{question.text} (копия)",
            test=question.test,
            has_one_correct_answer=question.has_one_correct_answer,
        )

        Answer.objects.bulk_create(
            [
                Answer(
                    text=answer.text,
                    is_correct=answer.is_correct,
                    question=new_question,
                )
                for answer in question.answers.all()
            ],
        )

        return redirect(
            reverse("admin:quizz_test_change", args=[question.test.pk]),
        )
