from typing import Any

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.quizz.api.serializers import TestSerializer
from src.apps.quizz.models.test_ import Test


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @csrf_exempt
    def retrieve(
        self,
        request: Response,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        return super().retrieve(request, *args, **kwargs)
