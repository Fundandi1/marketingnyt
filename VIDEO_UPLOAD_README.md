# Video Upload Guide

## Oversigt

Du kan nu uploade videoer til artikler på MarketingNyt.dk. Videoer kan uploades via:
1. **Wagtail Admin** (GUI)
2. **Python Script** (Programmatisk)

## Metode 1: Upload via Wagtail Admin

### Trin 1: Upload video
1. Gå til Wagtail admin: http://localhost:8000/admin/
2. Klik på **Snippets** i menuen
3. Klik på **Videos**
4. Klik på **Add Video**
5. Udfyld:
   - **Title**: Titel på videoen
   - **File**: Upload din video fil (.mp4, .webm, .mov)
   - **Thumbnail** (valgfrit): Upload et thumbnail billede
6. Klik **Save**

### Trin 2: Tilføj video til artikel
1. Gå til **Pages** i menuen
2. Find og rediger den artikel du vil tilføje video til
3. I **Cover video** feltet, vælg den video du lige uploadede
4. Klik **Publish**

**Vigtigt:** Hvis både Cover image og Cover video er sat, vil videoen blive vist i stedet for billedet.

## Metode 2: Upload via Python Script

### Forberedelse

1. **Placer din video fil** i `media/videos/` mappen:
   ```bash
   cp /path/to/your/video.mp4 media/videos/
   ```

2. **Valgfrit: Placer thumbnail** i `media/images/` mappen:
   ```bash
   cp /path/to/thumbnail.jpg media/images/
   ```

### Upload video med Python

#### Eksempel 1: Upload video uden at tilknytte til artikel

```python
from upload_video import upload_video

video = upload_video(
    video_path='media/videos/my-video.mp4',
    title='Min Marketing Video'
)
```

#### Eksempel 2: Upload video og tilknyt til artikel

```python
from upload_video import upload_video

video = upload_video(
    video_path='media/videos/facebook-ads.mp4',
    title='Facebook Ads Strategy Video',
    article_slug='facebook-ads-5-strategier-der-virker-i-2024',
    thumbnail_path='media/images/facebook-thumbnail.jpg'
)
```

### Find artikel slug

For at finde en artikels slug:

```python
from news.models import ArticlePage

# Vis alle artikler med deres slugs
articles = ArticlePage.objects.filter(live=True)
for article in articles:
    print(f'{article.title}: {article.slug}')
```

### Kør eksempel scriptet

```bash
python3 example_upload_video.py
```

## Video Formater

**Understøttede formater:**
- MP4 (anbefalet)
- WebM
- MOV
- AVI

**Anbefalinger:**
- **Format**: MP4 med H.264 codec
- **Opløsning**: 1920x1080 (Full HD) eller 1280x720 (HD)
- **Aspect ratio**: 16:9
- **Filstørrelse**: Under 100MB for bedste performance
- **Thumbnail**: 1280x720 pixels, JPG eller PNG

## Sådan konverterer du video til MP4

Hvis din video ikke er i MP4 format, kan du konvertere den med ffmpeg:

```bash
# Installer ffmpeg (hvis ikke allerede installeret)
brew install ffmpeg  # macOS
# eller
sudo apt-get install ffmpeg  # Linux

# Konverter video til MP4
ffmpeg -i input-video.mov -c:v libx264 -c:a aac -strict experimental output-video.mp4

# Komprimér stor video
ffmpeg -i input-video.mp4 -vcodec h264 -acodec aac -b:v 2M output-video.mp4
```

## Generer thumbnail fra video

```bash
# Generer thumbnail fra video (ved 5 sekunder)
ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 thumbnail.jpg
```

## Fejlfinding

### Video vises ikke
- Tjek at videoen er uploaded korrekt i Wagtail admin under Snippets > Videos
- Tjek at artiklen har `cover_video` sat (ikke kun `cover_image`)
- Tjek browser console for fejl

### Video er for stor
- Komprimér videoen med ffmpeg (se ovenfor)
- Overvej at hoste store videoer på YouTube/Vimeo i stedet

### Thumbnail vises ikke
- Tjek at thumbnail billedet er uploaded som et Wagtail Image
- Tjek at Video objektet har `thumbnail` feltet sat

## Eksempel: Komplet workflow

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from upload_video import upload_video
from news.models import ArticlePage

# 1. Find artikel
article = ArticlePage.objects.get(title__icontains='Facebook Ads')
print(f'Artikel slug: {article.slug}')

# 2. Upload video
video = upload_video(
    video_path='media/videos/facebook-ads-tutorial.mp4',
    title='Facebook Ads Tutorial 2024',
    article_slug=article.slug,
    thumbnail_path='media/images/facebook-thumbnail.jpg'
)

print(f'✅ Video uploaded og tilknyttet til artikel!')
print(f'Se artiklen på: http://localhost:8000/{article.slug}/')
```

## Video i Template

Videoen vises automatisk i `templates/news/article_page.html` med:
- HTML5 video player med controls
- Responsive 16:9 aspect ratio
- Thumbnail som poster image (hvis sat)
- Fallback til cover image hvis ingen video

## Administrer videoer

### Vis alle videoer
```python
from news.models import Video

videos = Video.objects.all()
for video in videos:
    print(f'{video.title}: {video.file.url}')
```

### Slet video
```python
from news.models import Video

video = Video.objects.get(title='Old Video')
video.delete()
```

### Opdater video på artikel
```python
from news.models import ArticlePage, Video

article = ArticlePage.objects.get(slug='my-article')
video = Video.objects.get(title='New Video')

article.cover_video = video
revision = article.save_revision()
revision.publish()
```

## Support

Hvis du har problemer, tjek:
1. Django logs: Se terminal hvor `python3 manage.py runserver` kører
2. Browser console: Åbn Developer Tools (F12) og tjek Console tab
3. Video fil: Tjek at filen eksisterer i `media/videos/` mappen

