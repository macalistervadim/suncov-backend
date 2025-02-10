from rest_framework import serializers

from src.apps.quizz.models.answer import Answer
from src.apps.quizz.models.question import Question
from src.apps.quizz.models.test_ import Test


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = "__all__"
