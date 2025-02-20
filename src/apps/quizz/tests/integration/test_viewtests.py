from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.quizz.models.test_ import Test


class TestViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_1 = Test.objects.create(title="Test 1")
        self.test_2 = Test.objects.create(title="Test 2")

    def test_get_all_tests(self) -> None:
        """Тестируем получение списка всех тестов"""
        response = self.client.get(reverse("test-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], self.test_1.title)
        self.assertEqual(response.data[1]["title"], self.test_2.title)
