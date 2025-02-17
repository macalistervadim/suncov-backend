from rest_framework import serializers

from src.apps.dictation.models.dictation import Dictation, Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "title")


class DictationSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(source="theme.title")

    class Meta:
        model = Dictation
        fields = ("id", "theme", "title", "text")
