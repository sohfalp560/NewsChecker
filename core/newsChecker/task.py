from celery import shared_task
from .models import NewsProvider, NewStory
from .scrapers import scrap_news_website

@shared_task
def scrap_news_task(instance_pk):
    try:
        instance = NewsProvider.objects.get(pk=instance_pk)
        stories = scrap_news_website(
            web_url=instance.website,
            story_class=instance.story_class,
            link_class=instance.link_class,
            title_class=instance.title_class,
            body_class=instance.body_class,
        )
        
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
        print(f"Task failed: {str(e)}")
        instance.status = NewsProvider.STATUS.failed
        instance.save(update_fields=['status'])