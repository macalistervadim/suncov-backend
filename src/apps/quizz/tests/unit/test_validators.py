from django.core.exceptions import ValidationError
from django.test import TestCase

from src.apps.dictation.models.dictation import Dictation, Theme
from src.apps.quizz.validators import AnswerInlineFormSet


class AnswerInlineFormSetTestCase(TestCase):
    def setUp(self) -> None:
        self.theme_one_correct = Theme.objects.create(title="Math")
        self.theme_multiple_correct = Theme.objects.create(title="Science")

        self.dictation_one_correct = Dictation.objects.create(
            theme=self.theme_one_correct,
            title="Dictation 1",
            text="Write the following words.",
        )
        self.dictation_multiple_correct = Dictation.objects.create(
            theme=self.theme_multiple_correct,
            title="Dictation 2",
            text="Write the following words.",
        )

    def test_one_correct_answer_mode(self) -> None:
        """Тестируем режим одного правильного ответа."""
        form_data = {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "0",
            **{
                f"form-{i}-is_correct": str(data["is_correct"])
                for i, data in enumerate(
                    [
                        {"is_correct": False},
                        {"is_correct": True},
                        {"is_correct": False},
                    ],
                )
            },
        }
        formset = AnswerInlineFormSet(
            data=form_data,
            instance=self.dictation_one_correct,
        )

        with self.assertRaises(ValidationError):
            formset.clean()

    def test_multiple_correct_answers_mode(self) -> None:
        """Тестируем режим нескольких правильных ответов."""
        form_data = {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            **{
                f"form-{i}-is_correct": str(data["is_correct"])
                for i, data in enumerate(
                    [
                        {"is_correct": False},
                        {"is_correct": True},
                    ],
                )
            },
        }
        formset = AnswerInlineFormSet(
            data=form_data,
            instance=self.dictation_multiple_correct,
        )

        try:
            formset.clean()
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly.")

    def test_multiple_correct_answers_mode_with_insufficient_correct_answers(
        self,
    ) -> None:
        """Тестируем режим нескольких правильных ответов с
        недостаточным количеством правильных вариантов."""
        form_data = {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            **{
                f"form-{i}-is_correct": str(data["is_correct"])
                for i, data in enumerate(
                    [
                        {"is_correct": False},
                        {"is_correct": False},
                    ],
                )
            },
        }
        formset = AnswerInlineFormSet(
            data=form_data,
            instance=self.dictation_multiple_correct,
        )

        with self.assertRaises(ValidationError):
            formset.clean()

    def test_no_answers(self) -> None:
        """Тестируем случай, когда нет выбранных правильных вариантов."""
        form_data = {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "0",
            **{
                f"form-{i}-is_correct": str(data["is_correct"])
                for i, data in enumerate(
                    [
                        {"is_correct": False},
                        {"is_correct": False},
                        {"is_correct": False},
                    ],
                )
            },
        }
        formset = AnswerInlineFormSet(
            data=form_data,
            instance=self.dictation_multiple_correct,
        )

        try:
            formset.clean()
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly.")
