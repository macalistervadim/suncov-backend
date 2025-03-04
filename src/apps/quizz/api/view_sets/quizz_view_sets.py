from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from src.apps.quizz.api.serializers import TestSerializer
from src.apps.quizz.models.test_ import Test


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]
