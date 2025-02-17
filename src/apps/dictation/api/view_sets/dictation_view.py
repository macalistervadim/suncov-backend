from collections import defaultdict
from typing import Any

from django.views.decorators.csrf import csrf_exempt
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

    @csrf_exempt
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        dictations = Dictation.objects.all()
        serialized_data = DictationSerializer(dictations, many=True).data

        grouped_data = defaultdict(list)

        for item in serialized_data:
            theme = item["theme"]
            grouped_data[theme].append(
                {"subtheme": item["title"], "text": item["text"]},
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

    @action(detail=False, methods=["get"])
    def by_theme(self, request: Request) -> Response:
        theme = request.query_params.get("theme", None)

        if theme:
            dictations = Dictation.objects.filter(theme_id=theme)

            if not dictations:
                return Response(
                    {"detail": "No dictations found for the given theme."},
                    status=404,
                )

            serialized_data = DictationSerializer(dictations, many=True).data

            grouped_data: defaultdict[str, dict[str, list]] = defaultdict(
                lambda: {"items": []},
            )

            for item in serialized_data:
                theme_title = item["theme"]
                grouped_data[theme_title]["items"].append(
                    {
                        "id": item["id"],
                        "text": item["text"],
                    },
                )

            result = [
                {"subtheme": theme, "items": data["items"]}
                for theme, data in grouped_data.items()
            ]

            return Response(result)

        else:
            return Response(
                {"detail": "Theme parameter is required."},
                status=400,
            )
