from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from src.apps.quizz.api.serializers import TestSerializer
from src.apps.quizz.models.test_ import Test


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
