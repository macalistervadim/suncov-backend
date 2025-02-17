from django.contrib import admin

from src.apps.dictation.models.dictation import Dictation, Theme


@admin.register(Dictation)
class DictationModelAdmin(admin.ModelAdmin):
    list_display = ("theme", "title")
    search_fields = ("title",)
    list_filter = ("theme",)


@admin.register(Theme)
class ThemeModelAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("title",)
