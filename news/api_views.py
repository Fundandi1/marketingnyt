"""
API views for automated content creation
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from wagtail.models import Page
from wagtail.images.models import Image
from .models import ArticlePage, Category, HomePage
import requests
from io import BytesIO
from django.core.files.images import ImageFile
import uuid


@csrf_exempt
@require_http_methods(["POST"])
def create_article_api(request):
    """
    API endpoint for creating articles via Make.com automation
    
    Expected JSON payload:
    {
        "title": "Article Title",
        "summary": "Article summary",
        "body": "Full article content in HTML",
        "category": "category-slug",
        "author": "Author Name",
        "cover_image_url": "https://example.com/image.jpg",
        "api_key": "your-secret-api-key"
    }
    """
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Validate API key
        expected_api_key = settings.AUTOMATION_API_KEY
        if data.get('api_key') != expected_api_key:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        # Required fields
        title = data.get('title')
        summary = data.get('summary')
        body = data.get('body')
        category_slug = data.get('category', 'marketing')
        author = data.get('author', 'MarketingNyt Redaktion')
        
        if not all([title, summary, body]):
            return JsonResponse({'error': 'Missing required fields: title, summary, body'}, status=400)
        
        # Get or create category
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            category = Category.objects.first()  # Fallback to first category
        
        # Get parent page (HomePage)
        home_page = HomePage.objects.first()
        if not home_page:
            return JsonResponse({'error': 'No homepage found'}, status=500)
        
        # Handle cover image if provided
        cover_image = None
        cover_image_url = data.get('cover_image_url')
        if cover_image_url:
            try:
                response = requests.get(cover_image_url, timeout=10)
                if response.status_code == 200:
                    image_file = ImageFile(BytesIO(response.content), name=f"article_{uuid.uuid4().hex[:8]}.jpg")
                    cover_image = Image(
                        title=f"Cover for {title}",
                        file=image_file
                    )
                    cover_image.save()
            except Exception as e:
                print(f"Failed to download image: {e}")
        
        # Create unique slug
        base_slug = title.lower().replace(' ', '-').replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
        base_slug = ''.join(c for c in base_slug if c.isalnum() or c == '-')[:50]
        slug = base_slug
        counter = 1
        while ArticlePage.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create article
        article = ArticlePage(
            title=title,
            slug=slug,
            summary=summary,
            body=body,
            category=category,
            author=author,
            cover_image=cover_image,
            is_featured=False,
            seo_title=title[:60],  # Limit for SEO
            search_description=summary[:160]  # Limit for meta description
        )
        
        # Add to homepage
        home_page.add_child(instance=article)
        
        # Publish the article
        article.save_revision().publish()
        
        return JsonResponse({
            'success': True,
            'article_id': article.id,
            'slug': article.slug,
            'url': article.get_full_url(),
            'message': f'Article "{title}" created and published successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_status(request):
    """Simple API status check"""
    return JsonResponse({
        'status': 'ok',
        'message': 'MarketingNyt API is running',
        'endpoints': {
            'create_article': '/api/create-article/',
            'status': '/api/status/'
        }
    })
