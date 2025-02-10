from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.quizz.api.view_sets.answer_view import AnswerViewSet
from src.apps.quizz.api.view_sets.question_view import QuestionViewSet
from src.apps.quizz.api.view_sets.test_view import TestViewSet

router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="test")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"answers", AnswerViewSet, basename="answers")

urlpatterns = [
    path("", include(router.urls)),
]
