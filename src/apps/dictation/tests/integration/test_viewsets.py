from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from src.apps.dictation.models.dictation import Dictation, Theme


class DictationViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.theme = Theme.objects.create(title="Math")
        self.dictation1 = Dictation.objects.create(
            theme=self.theme,
            title="Spelling Test 1",
            text="Write the following words.",
        )
        self.dictation2 = Dictation.objects.create(
            theme=self.theme,
            title="Spelling Test 2",
            text="Write the following words.",
        )

        self.client = APIClient()

    def test_list_dictations(self) -> None:
        """
        Тестирует получение списка диктантов.
        Проверяем, что данные возвращаются группированные по теме.
        """
        url = reverse("dictation-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(
            isinstance(data, list),
        )
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["theme"], self.theme.title,
        )
        self.assertEqual(len(data[0]["items"]), 2)

    def test_by_theme_with_valid_theme(self) -> None:
        """
        Тестирует фильтрацию по теме с корректным параметром.
        """
        url = reverse(
            "dictation-by-theme",
        )
        response = self.client.get(f"{url}?theme={self.theme.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["subtheme"], self.theme.title,
        )
        self.assertEqual(len(data[0]["items"]), 2)

    def test_by_theme_with_invalid_theme(self) -> None:
        """
        Тестирует фильтрацию по теме с несуществующей темой.
        """
        url = reverse(
            "dictation-by-theme",
        )
        response = self.client.get(f"{url}?theme=9999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.json()
        self.assertEqual(
            data["detail"], "No dictations found for the given theme.",
        )

    def test_by_theme_without_theme_param(self) -> None:
        """
        Тестирует фильтрацию по теме без параметра 'theme'.
        """
        url = reverse(
            "dictation-by-theme",
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["detail"], "Theme parameter is required.")
