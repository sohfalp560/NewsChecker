from django.contrib import admin

from .models import NewsProvider, NewStory


@admin.register(NewsProvider)
class NewsProviderAdmin(admin.ModelAdmin):
    list_display = [
        "website",
        "last_time_checked",
        "status",
        "story_class",
        "link_class",
        "title_class",
        "body_class",
    ]


@admin.register(NewStory)
class NewStoryAdmin(admin.ModelAdmin):
    list_display = [
        "story_link",
        "title",
        "body",
        "website",
        "download_time",
    ]
