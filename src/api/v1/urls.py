from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.dictation.api.view_sets.dictation_view import DictationView
from src.apps.partofspeech.api.view_sets.part_of_speech_view import (
    PartOfSpeechView,
)
from src.apps.quizz.api.view_sets.quizz_view_sets import TestViewSet

router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="test")
router.register(r"dictations", DictationView, basename="dictation")
router.register(
    r"part_of_speechs",
    PartOfSpeechView,
    basename="part-of-speech",
)

urlpatterns = [
    path("", include(router.urls)),
]
