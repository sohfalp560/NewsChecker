from django.db import models, transaction

# from django.contrib.auth import user
from django.db.models.signals import post_save
from django.dispatch import receiver

# https://t.me/M23632M
from .scrapers import scrap_news_website


class NewsProvider(models.Model):
    class STATUS(models.TextChoices):
        ok = "OK", "Updated!"
        failed = "FA", "failed!"
        not_started = "NS", "not started!"

    website = models.URLField(max_length=200, blank=False, null=False, unique=True)
    last_time_checked = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS.not_started)
    story_class = models.CharField(max_length=40, blank=True, null=True)
    link_class = models.CharField(max_length=40, blank=True, null=True)
    title_class = models.CharField(max_length=40, blank=True, null=True)
    body_class = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name_plural = "News Providers"

    def __str__(self):
        return f"news source: {self.website}"

    def save(self, *args, **kwargs):
        print(f"the model is saved@ {self.website}")
        return super().save(*args, **kwargs)


class NewStory(models.Model):
    story_link = models.URLField(max_length=500,unique=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    website = models.ForeignKey(
        NewsProvider, related_name="news_story", on_delete=models.CASCADE
    )
    download_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ['-download_time']

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


@receiver(post_save, sender=NewsProvider)
def create_stories_from_website(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: scrap_news_website(instance.pk))

"""because it is moved to task.py:
def scrap_save(instance_pk):
    print("the signal start")
    try:
        instance = NewsProvider.objects.get(pk=instance_pk)
        stories = scrap_news_website(
            web_url=instance.website,
            story_class=instance.story_class,
            link_class=instance.link_class,
            title_class=instance.title_class,
            body_class=instance.body_class,
        )
        print("the signal scraped")

        bulk_stories = [
            NewStory(
                website=instance,
                story_link=story.get("link", ""),
                title=story.get("title", "No title"),
                body=story.get("body", "No content"),
            )
            for story in stories
        ]
        NewStory.objects.bulk_create(bulk_stories)

        instance.status = NewsProvider.STATUS.ok
        instance.save(update_fields=['status'])

    except Exception as e:
        print(f"Scraping failed: {str(e)}")

        instance.status = NewsProvider.STATUS.failed
        instance.save(update_fields=['status'])
"""