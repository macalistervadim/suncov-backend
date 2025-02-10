from rest_framework import viewsets

from src.apps.quizz.api.serializers import AnswerSerializer
from src.apps.quizz.models.answer import Answer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
