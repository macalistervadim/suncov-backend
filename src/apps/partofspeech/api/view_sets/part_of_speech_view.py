from collections import defaultdict
from typing import Any

from django.views.decorators.csrf import csrf_exempt
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

    @csrf_exempt
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        dictations = PartOfSpeech.objects.all()
        serialized_data = PartOfSpeechSerializer(dictations, many=True).data

        grouped_data = defaultdict(list)

        for item in serialized_data:
            theme = item["theme"]
            grouped_data[theme].append(
                {"text": item["text"]},
            )

        result = [
            {"theme": theme, "items": items}
            for theme, items in grouped_data.items()
        ]


        return Response(result)

    @csrf_exempt
    def retrieve(
        self,
        request: Response,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        return super().retrieve(request, *args, **kwargs)
