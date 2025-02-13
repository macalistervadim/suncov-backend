from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.quizz.api.view_sets.test_view import TestViewSet

router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="test")

urlpatterns = [
    path("", include(router.urls)),
]
