from typing import Any

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.partofspeech.api.serializers import PartOfSpeechSerializer
from src.apps.partofspeech.models.part_of_speech import PartOfSpeech


class PartOfSpeechView(viewsets.ReadOnlyModelViewSet):
    queryset = PartOfSpeech.objects.all()
    serializer_class = PartOfSpeechSerializer
    permission_classes = [AllowAny]

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        parts_of_speech = PartOfSpeech.objects.all()
        serialized_data = PartOfSpeechSerializer(
            parts_of_speech, many=True,
        ).data

        grouped_data: dict[Any, Any] = {}
        for item in serialized_data:
            theme = item["theme"]
            if theme not in grouped_data:
                grouped_data[theme] = []
            grouped_data[theme].append({"text": item["text"]})

        result = [
            {"theme": theme, "items": items}
            for theme, items in grouped_data.items()
        ]
        return Response(result)
