from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from src.apps.partofspeech.models.part_of_speech import PartOfSpeech, Theme


class PartOfSpeechViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.theme1 = Theme.objects.create(title="Grammatical")
        self.theme2 = Theme.objects.create(title="Lexical")
        self.part_of_speech1 = PartOfSpeech.objects.create(
            theme=self.theme1,
            text="Adjectives are descriptive words.",
        )
        self.part_of_speech2 = PartOfSpeech.objects.create(
            theme=self.theme1,
            text="Nouns are naming words.",
        )
        self.part_of_speech3 = PartOfSpeech.objects.create(
            theme=self.theme2,
            text="Verbs indicate actions.",
        )

        self.client = APIClient()

    def test_list_parts_of_speech(self) -> None:
        """
        Тестирует получение списка частей речи, проверяя,
        что данные сгруппированы по теме.
        """
        url = reverse("part-of-speech-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["theme"], self.theme1.title)
        self.assertEqual(len(data[0]["items"]), 2)

        self.assertEqual(data[1]["theme"], self.theme2.title)
        self.assertEqual(len(data[1]["items"]), 1)

    def test_list_parts_of_speech_empty(self) -> None:
        """
        Тестирует получение списка частей речи, если нет данных.
        """
        PartOfSpeech.objects.all().delete()

        url = reverse("part-of-speech-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data, [])

    def test_list_parts_of_speech_no_groups(self) -> None:
        """
        Тестирует получение списка частей речи без группировки,
        когда все части речи имеют одинаковую тему.
        """
        self.part_of_speech3.delete()

        url = reverse("part-of-speech-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["theme"], self.theme1.title)
        self.assertEqual(len(data[0]["items"]), 3)
