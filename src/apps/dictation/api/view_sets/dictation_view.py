from collections import defaultdict
from typing import Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.dictation.api.serializers import DictationSerializer
from src.apps.dictation.models.dictation import Dictation


class DictationView(viewsets.ReadOnlyModelViewSet):
    queryset = Dictation.objects.all()
    serializer_class = DictationSerializer
    permission_classes = [AllowAny]

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serialized_data = self.get_serializer(
            self.get_queryset(), many=True,
        ).data
        grouped_data = defaultdict(list)

        for item in serialized_data:
            grouped_data[item["theme"]].append(
                {"subtheme": item["title"], "text": item["text"]},
            )

        result = [
            {"theme": theme, "items": items}
            for theme, items in grouped_data.items()
        ]
        return Response(result)

    @action(detail=False, methods=["get"])
    def by_theme(self, request: Request) -> Response:
        theme = request.query_params.get("theme")
        if not theme:
            return Response(
                {"detail": "Theme parameter is required."}, status=400,
            )

        dictations = Dictation.objects.filter(theme_id=theme)
        if not dictations.exists():
            return Response(
                {"detail": "No dictations found for the given theme."},
                status=404,
            )

        serialized_data = self.get_serializer(dictations, many=True).data
        grouped_data = defaultdict(list)

        for item in serialized_data:
            grouped_data[item["theme"]].append(
                {"id": item["id"], "text": item["text"]},
            )

        result = [
            {"subtheme": theme, "items": items}
            for theme, items in grouped_data.items()
        ]
        return Response(result)
