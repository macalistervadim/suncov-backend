from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class URLAccessibilityTestCase(APITestCase):
    def test_test_view_url(self) -> None:
        url = reverse("test-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dictation_view_url(self) -> None:
        url = reverse("dictation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_part_of_speech_view_url(self) -> None:
        url = reverse("part-of-speech-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
