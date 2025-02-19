from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.quizz.models.test_ import Test


class TestViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_1 = Test.objects.create(title="Test 1")
        self.test_2 = Test.objects.create(title="Test 2")
        self.url = "/api/tests/"
        self.single_url = (
            f"/api/tests/{self.test_1.id}/"
        )

    def test_get_all_tests(self) -> None:
        """Тестируем получение списка всех тестов"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], self.test_1.title)
        self.assertEqual(response.data[1]["title"], self.test_2.title)

    def test_get_single_test(self) -> None:
        """Тестируем получение одного теста"""
        response = self.client.get(self.single_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.test_1.title)

    def test_get_nonexistent_test(self) -> None:
        """Тестируем получение несуществующего теста"""
        non_existent_url = "/api/tests/999/"
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_test_not_allowed(self) -> None:
        """Тестируем попытку создания теста,
        которое не разрешено в ReadOnlyModelViewSet"""
        data = {
            "title": "Test 3",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_update_test_not_allowed(self) -> None:
        """Тестируем попытку обновления теста,
        которое не разрешено в ReadOnlyModelViewSet"""
        data = {
            "title": "Updated Test 1",
        }
        response = self.client.put(self.single_url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_delete_test_not_allowed(self) -> None:
        """Тестируем попытку удаления теста,
        которое не разрешено в ReadOnlyModelViewSet"""
        response = self.client.delete(self.single_url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )
