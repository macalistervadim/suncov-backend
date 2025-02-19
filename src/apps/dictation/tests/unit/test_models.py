from django.db.utils import IntegrityError
from django.test import TestCase

from src.apps.dictation.models.dictation import Dictation, Theme


class ThemeModelTest(TestCase):
    def setUp(self) -> None:
        """Создание базовых данных для тестов."""
        self.theme = Theme.objects.create(title="Grammar")

    def test_theme_str(self) -> None:
        """Тестирование метода __str__"""
        self.assertEqual(str(self.theme), "Grammar")

    def test_theme_repr(self) -> None:
        """Тестирование метода __repr__"""
        self.assertEqual(repr(self.theme), "Theme(title='Grammar')")

    def test_theme_unique_title(self) -> None:
        """Проверка, что тема с таким же названием не может быть создана"""
        with self.assertRaises(IntegrityError):
            Theme.objects.create(title="Grammar")


class DictationModelTest(TestCase):
    def setUp(self) -> None:
        """Создание базовых данных для тестов."""
        self.theme = Theme.objects.create(title="Grammar")
        self.dictation = Dictation.objects.create(
            theme=self.theme,
            title="Test Dictation",
            text="This is a test text.",
        )

    def test_dictation_str(self) -> None:
        """Тестирование метода __str__"""
        self.assertEqual(str(self.dictation), "Test Dictation")

    def test_dictation_repr(self) -> None:
        """Тестирование метода __repr__"""
        self.assertEqual(
            repr(self.dictation),
            "Dictation(theme=<Theme: Grammar>, "
            "title='Test Dictation', text='This is a test text.')",
        )

    def test_dictation_foreign_key(self) -> None:
        """Проверка, что связанная тема корректно отображается"""
        self.assertEqual(self.dictation.theme.title, "Grammar")

    def test_dictation_unique_title(self) -> None:
        """Проверка, что диктант с таким же названием не может быть создан"""
        with self.assertRaises(IntegrityError):
            Dictation.objects.create(
                theme=self.theme,
                title="Test Dictation",
                text="Some other text.",
            )

    def test_dictation_empty_text(self) -> None:
        """Проверка, что текст диктанта не может быть пустым"""
        with self.assertRaises(ValueError):
            Dictation.objects.create(
                theme=self.theme, title="Empty Text Dictation", text="",
            )

    def test_dictation_relation_with_theme(self) -> None:
        """Проверка, что при удалении темы удаляются все связанные диктанты"""
        self.dictation.delete()
        with self.assertRaises(Dictation.DoesNotExist):
            Dictation.objects.get(title="Test Dictation")
