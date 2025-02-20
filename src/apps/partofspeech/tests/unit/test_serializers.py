from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.apps.partofspeech.api.serializers import PartOfSpeechSerializer


class PartOfSpeechSerializerTestCase(APITestCase):
    def test_part_of_speech_serializer_valid(self) -> None:
        data = {
            "id": 1,
            "theme": "Grammar",
            "text": "Noun: A person, place, or thing.",
        }

        serializer = PartOfSpeechSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        self.assertEqual(serialized_data["theme"], data["theme"])
        self.assertEqual(serialized_data["text"], data["text"])

    def test_part_of_speech_serializer_invalid_data(self) -> None:
        """
        Тестирует сериализацию с некорректными данными.
        Проверяет, что сериализатор выбрасывает ошибку при неправильных данных.
        """
        invalid_data = {
            "theme": "",
            "text": "",
        }

        serializer = PartOfSpeechSerializer(data=invalid_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
