from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.dictation.api.view_sets.dictation_view import DictationView
from src.apps.partofspeech.api.view_sets.part_of_speech_view import (
    PartOfSpeechView,
)
from src.apps.quizz.api.view_sets.test_view import TestViewSet

router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="test")
router.register(r"dictations", DictationView, basename="dication")
router.register(r"part_of_speechs", PartOfSpeechView, basename="part-of-speech")

urlpatterns = [
    path("", include(router.urls)),
]
