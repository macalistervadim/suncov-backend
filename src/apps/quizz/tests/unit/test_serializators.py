from typing import Any

from rest_framework.test import APITestCase

from src.apps.quizz.api.serializers import (
    AnswerSerializer,
    QuestionSerializer,
    TestSerializer,
)
from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class AnswerSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        self.test = Test.objects.create(title="Sample Test")
        self.question = Question.objects.create(
            text="What is 2 + 2?",
            test=self.test,
            has_one_correct_answer=True,
        )
        self.answer_data = {
            "text": "4",
            "is_correct": True,
            "question": self.question.id,
        }

    def test_answer_serializer_valid_data(self) -> None:
        """Тестируем сериализатор с валидными данными"""
        serializer = AnswerSerializer(data=self.answer_data)
        self.assertTrue(serializer.is_valid())
        answer = serializer.save()
        self.assertEqual(answer.text, "4")
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.question, self.question)

    def test_answer_serializer_invalid_data(self) -> None:
        """Тестируем сериализатор с невалидными данными
        (без обязательного поля)"""
        invalid_data = {
            "text": "4",
            "is_correct": True,
        }
        serializer = AnswerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("question", serializer.errors)

    def test_answer_serializer_representation(self) -> None:
        """Тестируем корректное представление данных"""
        answer = Answer.objects.create(
            text="4",
            is_correct=True,
            question=self.question,
        )
        serializer = AnswerSerializer(answer)
        self.assertEqual(serializer.data["text"], "4")
        self.assertEqual(serializer.data["is_correct"], True)
        self.assertEqual(serializer.data["question"], self.question.id)


class QuestionSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        """Настройка тестовых данных"""
        self.test = Test.objects.create(title="Sample Test")
        self.question_data = {
            "text": "What is 2 + 2?",
            "test": self.test.id,
            "has_one_correct_answer": True,
            "answers": [
                {
                    "text": "4",
                    "is_correct": True,
                    "question": self.test.id,
                },
            ],
        }

    def test_question_serializer_valid_data(self) -> None:
        """Тестируем сериализатор с валидными данными"""
        serializer = QuestionSerializer(data=self.question_data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()
        self.assertEqual(question.text, "What is 2 + 2?")
        self.assertEqual(question.test, self.test)
        self.assertTrue(question.has_one_correct_answer)
        self.assertEqual(len(question.answers.all()), 1)

    def test_question_serializer_invalid_data(self) -> None:
        """Тестируем сериализатор с невалидными данными
        (без обязательного поля)"""
        invalid_data = {
            "text": "What is 3 + 3?",
            "has_one_correct_answer": True,
        }
        serializer = QuestionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("test", serializer.errors)

    def test_question_serializer_representation(self) -> None:
        """Тестируем корректное представление данных"""
        question = Question.objects.create(
            text="What is 2 + 2?",
            test=self.test,
            has_one_correct_answer=True,
        )
        serializer = QuestionSerializer(question)
        self.assertEqual(serializer.data["text"], "What is 2 + 2?")
        self.assertEqual(serializer.data["test"], self.test.id)


class TestSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_data = {
            "title": "Sample Test",
            "questions": [
                {
                    "text": "What is 2 + 2?",
                    "test": None,
                    "has_one_correct_answer": True,
                    "answers": [
                        {
                            "text": "4",
                            "is_correct": True,
                            "question": None,
                        },
                    ],
                },
            ],
        }

    def test_test_serializer_valid_data(self) -> None:
        """Тестируем сериализатор с валидными данными"""
        serializer = TestSerializer(data=self.test_data)
        self.assertTrue(serializer.is_valid())
        test_obj = serializer.save()
        self.assertEqual(test_obj.title, "Sample Test")
        self.assertEqual(len(test_obj.questions.all()), 1)

    def test_test_serializer_invalid_data(self) -> None:
        """Тестируем сериализатор с невалидными данными
        (без обязательного поля)"""
        invalid_data: dict[str, list[Any]] = {
            "questions": [],
        }
        serializer = TestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_test_serializer_representation(self) -> None:
        """Тестируем корректное представление данных"""
        test_obj = Test.objects.create(title="Sample Test")
        Question.objects.create(
            text="What is 2 + 2?",
            test=test_obj,
            has_one_correct_answer=True,
        )
        serializer = TestSerializer(test_obj)
        self.assertEqual(serializer.data["title"], "Sample Test")
        self.assertEqual(len(serializer.data["questions"]), 1)
