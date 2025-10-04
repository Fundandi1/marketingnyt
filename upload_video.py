import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from django.core.files import File
from news.models import Video, ArticlePage
from wagtail.images.models import Image

def upload_video(video_path, title, article_slug=None, thumbnail_path=None):
    """
    Upload a video and optionally attach it to an article.
    
    Args:
        video_path: Path to the video file
        title: Title for the video
        article_slug: Optional slug of the article to attach video to
        thumbnail_path: Optional path to thumbnail image
    
    Returns:
        Video object
    """
    
    # Check if video file exists
    if not os.path.exists(video_path):
        print(f'❌ Video file not found: {video_path}')
        return None
    
    # Create or get video
    with open(video_path, 'rb') as video_file:
        video = Video()
        video.title = title
        video.file.save(os.path.basename(video_path), File(video_file), save=False)
        
        # Add thumbnail if provided
        if thumbnail_path and os.path.exists(thumbnail_path):
            with open(thumbnail_path, 'rb') as thumb_file:
                thumbnail = Image()
                thumbnail.title = f"{title} - Thumbnail"
                thumbnail.file.save(os.path.basename(thumbnail_path), File(thumb_file), save=True)
                video.thumbnail = thumbnail
        
        video.save()
        print(f'✅ Video uploaded: {video.title} (ID: {video.id})')
    
    # Attach to article if slug provided
    if article_slug:
        try:
            article = ArticlePage.objects.get(slug=article_slug)
            article.cover_video = video
            revision = article.save_revision()
            revision.publish()
            print(f'✅ Video attached to article: {article.title}')
        except ArticlePage.DoesNotExist:
            print(f'❌ Article not found with slug: {article_slug}')
    
    return video


# Example usage:
if __name__ == '__main__':
    # Upload a video
    # video = upload_video(
    #     video_path='path/to/your/video.mp4',
    #     title='My Video Title',
    #     article_slug='article-slug',  # Optional
    #     thumbnail_path='path/to/thumbnail.jpg'  # Optional
    # )
    
    print('=== VIDEO UPLOAD SCRIPT ===')
    print()
    print('Usage:')
    print('  from upload_video import upload_video')
    print()
    print('  # Upload video only')
    print('  video = upload_video(')
    print('      video_path="media/videos/my-video.mp4",')
    print('      title="My Video Title"')
    print('  )')
    print()
    print('  # Upload video and attach to article')
    print('  video = upload_video(')
    print('      video_path="media/videos/my-video.mp4",')
    print('      title="My Video Title",')
    print('      article_slug="facebook-ads-5-strategier",')
    print('      thumbnail_path="media/images/thumbnail.jpg"')
    print('  )')

