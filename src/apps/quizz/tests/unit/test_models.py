from django.test import TestCase

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class TestModelTestCase(TestCase):
    def setUp(self) -> None:
        self.test_obj = Test.objects.create(title="Sample Test")

    def test_create_test(self) -> None:
        """Тестируем создание объекта Test"""
        self.assertEqual(self.test_obj.title, "Sample Test")
        self.assertIsInstance(self.test_obj, Test)
        self.assertEqual(str(self.test_obj), "Sample Test")

    def test_repr_test(self) -> None:
        """Тестируем __repr__ метод"""
        expected_repr = "Test(title='Sample Test')"
        self.assertEqual(repr(self.test_obj), expected_repr)

    def test_string_representation(self) -> None:
        """Тестируем __str__ метод"""
        self.assertEqual(str(self.test_obj), "Sample Test")

    def test_meta_verbose_name(self) -> None:
        """Тестируем Meta.verbose_name"""
        self.assertEqual(self.test_obj._meta.verbose_name, "Test")
        self.assertEqual(self.test_obj._meta.verbose_name_plural, "Tests")

    def test_unique_title(self) -> None:
        """Тестируем уникальность поля title"""
        with self.assertRaises(Exception):
            Test.objects.create(
                title="Sample Test",
            )


class QuestionModelTestCase(TestCase):
    def setUp(self) -> None:
        self.test_obj = Test.objects.create(title="Sample Test")
        self.question = Question.objects.create(
            text="What is 2 + 2?",
            test=self.test_obj,
            has_one_correct_answer=True,
        )

    def test_create_question(self) -> None:
        """Тестируем создание объекта Question"""
        self.assertEqual(self.question.text, "What is 2 + 2?")
        self.assertEqual(self.question.test, self.test_obj)
        self.assertTrue(self.question.has_one_correct_answer)
        self.assertIsInstance(self.question, Question)

    def test_repr_question(self) -> None:
        """Тестируем __repr__ метод"""
        expected_repr = (
            f"Question(test={self.test_obj!r}, "
            f"text='What is 2 + 2?', "
            f"has_one_correct_answer=True)"
        )
        self.assertEqual(repr(self.question), expected_repr)

    def test_string_representation(self) -> None:
        """Тестируем __str__ метод"""
        self.assertEqual(str(self.question), "What is 2 + 2?")

    def test_meta_verbose_name(self) -> None:
        """Тестируем Meta.verbose_name"""
        self.assertEqual(self.question._meta.verbose_name, "Question")
        self.assertEqual(self.question._meta.verbose_name_plural, "Questions")

    def test_boolean_field_default(self) -> None:
        """Тестируем значение поля по умолчанию для has_one_correct_answer"""
        question = Question.objects.create(
            text="What is 3 + 3?",
            test=self.test_obj,
        )
        self.assertTrue(
            question.has_one_correct_answer,
        )


class AnswerModelTestCase(TestCase):
    def setUp(self) -> None:
        self.test_obj = Test.objects.create(title="Sample Test")
        self.question = Question.objects.create(
            text="What is 2 + 2?",
            test=self.test_obj,
            has_one_correct_answer=True,
        )
        self.answer = Answer.objects.create(
            text="4",
            is_correct=True,
            question=self.question,
        )

    def test_create_answer(self) -> None:
        """Тестируем создание объекта Answer"""
        self.assertEqual(self.answer.text, "4")
        self.assertTrue(self.answer.is_correct)
        self.assertEqual(self.answer.question, self.question)
        self.assertIsInstance(self.answer, Answer)

    def test_repr_answer(self) -> None:
        """Тестируем __repr__ метод"""
        expected_repr = (
            f"Answer(question={self.question!r}, text='4', is_correct=True)"
        )
        self.assertEqual(repr(self.answer), expected_repr)

    def test_string_representation(self) -> None:
        """Тестируем __str__ метод"""
        self.assertEqual(str(self.answer), "4")

    def test_meta_verbose_name(self) -> None:
        """Тестируем Meta.verbose_name"""
        self.assertEqual(self.answer._meta.verbose_name, "Answer")
        self.assertEqual(self.answer._meta.verbose_name_plural, "Answers")

    def test_boolean_field_default(self) -> None:
        """Тестируем значение поля по умолчанию для is_correct"""
        answer = Answer.objects.create(
            text="5",
            question=self.question,
        )
        self.assertFalse(answer.is_correct)
