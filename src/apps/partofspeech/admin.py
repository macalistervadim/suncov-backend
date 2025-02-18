from django.contrib import admin

from src.apps.partofspeech.models.part_of_speech import PartOfSpeech, Theme


@admin.register(PartOfSpeech)
class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ("theme__title",)
    search_fields = ("theme__title",)
    list_filter = ("theme__title",)
    ordering = ("-theme__title",)
    list_per_page = 20


@admin.register(Theme)
class ThemePartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("title",)
    ordering = ("-title",)
    list_per_page = 20
