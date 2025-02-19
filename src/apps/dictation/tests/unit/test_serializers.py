from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.apps.dictation.api.serializers import (
    DictationSerializer,
    ThemeSerializer,
)
from src.apps.dictation.models.dictation import Dictation, Theme


class ThemeSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        self.theme_data = {"title": "Math"}
        self.theme = Theme.objects.create(**self.theme_data)

    def test_theme_serializer_valid(self) -> None:
        serializer = ThemeSerializer(self.theme)
        self.assertEqual(
            serializer.data,
            {"id": self.theme.id, "title": self.theme.title},
        )

    def test_theme_serializer_invalid(self) -> None:
        invalid_data = {"title": ""}
        serializer = ThemeSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class DictationSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        theme = Theme.objects.create(title="Math")
        self.dictation_data = {
            "theme": theme,
            "title": "Spelling Test",
            "text": "Write the following words correctly.",
        }
        self.dictation = Dictation.objects.create(**self.dictation_data)

    def test_dictation_serializer_valid(self) -> None:
        serializer = DictationSerializer(self.dictation)
        self.assertEqual(
            serializer.data,
            {
                "id": self.dictation.id,
                "theme": self.dictation.theme.title,
                "title": self.dictation.title,
                "text": self.dictation.text,
            },
        )

    def test_dictation_serializer_invalid(self) -> None:
        invalid_data = {"theme": None, "title": "", "text": ""}
        serializer = DictationSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
