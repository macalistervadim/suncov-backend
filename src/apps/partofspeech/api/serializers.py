from rest_framework import serializers

from src.apps.partofspeech.models.part_of_speech import PartOfSpeech


class PartOfSpeechSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(source="theme.title")

    class Meta:
        model = PartOfSpeech
        fields = ("id", "theme", "text")
