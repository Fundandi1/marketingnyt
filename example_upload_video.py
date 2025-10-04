"""
Example script showing how to upload videos to articles.

Before running this script:
1. Place your video file in the media/videos/ folder (create folder if needed)
2. Optionally place a thumbnail image in media/images/
3. Update the paths and article slug below
4. Run: python3 example_upload_video.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from upload_video import upload_video

# Example 1: Upload video without attaching to article
print('=== EXAMPLE 1: Upload video only ===')
video1 = upload_video(
    video_path='media/videos/example-video.mp4',  # Change this to your video path
    title='Example Marketing Video'
)

# Example 2: Upload video and attach to specific article
print('\n=== EXAMPLE 2: Upload video and attach to article ===')
video2 = upload_video(
    video_path='media/videos/facebook-ads-video.mp4',  # Change this to your video path
    title='Facebook Ads Strategy Video',
    article_slug='facebook-ads-5-strategier-der-virker-i-2024',  # Change to your article slug
    thumbnail_path='media/images/facebook-thumbnail.jpg'  # Optional thumbnail
)

print('\n=== DONE ===')
print('Videos uploaded successfully!')
print('You can now view them in the Wagtail admin under Snippets > Videos')

