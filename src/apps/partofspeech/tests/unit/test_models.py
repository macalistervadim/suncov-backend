from django.test import TestCase

from src.apps.partofspeech.models.part_of_speech import PartOfSpeech, Theme


class PartOfSpeechModelTestCase(TestCase):
    def setUp(self) -> None:
        self.theme = Theme.objects.create(title="Grammar")
        self.part_of_speech = PartOfSpeech.objects.create(
            theme=self.theme,
            text="Noun: A person, place, or thing.",
        )

    def test_part_of_speech_creation(self) -> None:
        """
        Тестирует создание объекта PartOfSpeech.
        Проверяем, что объект был успешно создан и сохранен в базе данных.
        """
        part_of_speech = self.part_of_speech
        self.assertEqual(
            part_of_speech.theme,
            self.theme,
        )
        self.assertEqual(
            part_of_speech.text,
            "Noun: A person, place, or thing.",
        )

    def test_str_method(self) -> None:
        """
        Тестирует метод __str__ модели PartOfSpeech.
        Проверяем, что строковое представление объекта правильное.
        """
        part_of_speech = self.part_of_speech
        self.assertEqual(
            str(part_of_speech),
            f"{self.theme} - {part_of_speech.text[:50]}",
        )

    def test_repr_method(self) -> None:
        """
        Тестирует метод __repr__ модели PartOfSpeech.
        Проверяем, что представление объекта правильное.
        """
        part_of_speech = self.part_of_speech
        self.assertEqual(
            repr(part_of_speech),
            f"PartOfSpeech(theme={self.theme!r}, "
            f"text={part_of_speech.text!r})",
        )
