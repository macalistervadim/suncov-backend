from rest_framework import viewsets

from src.apps.quizz.api.serializers import QuestionSerializer
from src.apps.quizz.models.question import Question


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
