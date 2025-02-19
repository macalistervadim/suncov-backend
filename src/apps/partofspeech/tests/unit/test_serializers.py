from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.apps.partofspeech.api.serializers import PartOfSpeechSerializer


class PartOfSpeechSerializerTestCase(APITestCase):
    """
    Тестирование сериализатора PartOfSpeechSerializer.
    """

    def test_part_of_speech_serializer_valid(self) -> None:
        """
        Тестирует сериализацию правильных данных.
        Проверяет, что сериализатор правильно сериализует данные в JSON.
        """
        data = {
            "id": 1,
            "theme": "Grammar",
            "text": "Noun: A person, place, or thing.",
        }

        serializer = PartOfSpeechSerializer(data)
        serialized_data = serializer.data

        self.assertEqual(serialized_data["id"], data["id"])
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

    def test_part_of_speech_serializer_partial_update(self) -> None:
        """
        Тестирует частичное обновление данных с помощью сериализатора.
        Проверяет, что сериализатор может обновить только часть данных.
        """
        initial_data = {
            "id": 1,
            "theme": "Grammar",
            "text": "Noun: A person, place, or thing.",
        }

        updated_data = {"text": "Updated text for part of speech."}

        serializer = PartOfSpeechSerializer(initial_data)
        self.assertEqual(serializer.data["text"], initial_data["text"])

        updated_serializer = PartOfSpeechSerializer(
            initial_data, data=updated_data, partial=True,
        )
        updated_serializer.is_valid(raise_exception=True)
        updated_part_of_speech = updated_serializer.save()

        self.assertEqual(updated_part_of_speech["text"], updated_data["text"])

    def test_part_of_speech_serializer_create(self) -> None:
        """
        Тестирует создание нового объекта с помощью сериализатора.
        Проверяет, что сериализатор может создать новый объект.
        """
        new_data = {
            "theme": "Syntax",
            "text": "Adjective: A word that describes a noun.",
        }

        serializer = PartOfSpeechSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())
        created_part_of_speech = serializer.save()

        self.assertEqual(created_part_of_speech["theme"], new_data["theme"])
        self.assertEqual(created_part_of_speech["text"], new_data["text"])
