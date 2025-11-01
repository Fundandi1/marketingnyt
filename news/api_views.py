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
import urllib.parse


def get_marketing_image(title, category="marketing"):
    """
    Get a relevant marketing image from Unsplash based on title and category
    """
    try:
        # Marketing-related search terms based on category
        marketing_terms = {
            'digital-marketing': ['digital marketing', 'online marketing', 'social media'],
            'seo': ['seo', 'search engine', 'google analytics'],
            'social-media': ['social media', 'instagram', 'facebook marketing'],
            'content-marketing': ['content marketing', 'blogging', 'copywriting'],
            'email-marketing': ['email marketing', 'newsletter', 'email campaign'],
            'analytics': ['analytics', 'data visualization', 'charts'],
            'marketing': ['marketing', 'business', 'strategy']
        }

        # Get search terms for category
        search_terms = marketing_terms.get(category, marketing_terms['marketing'])
        search_query = search_terms[0]  # Use first term

        # Unsplash API endpoint (free tier - no API key needed for basic usage)
        unsplash_url = f"https://source.unsplash.com/1200x600/?{urllib.parse.quote(search_query)}"

        # Download image
        response = requests.get(unsplash_url, timeout=10)
        if response.status_code == 200:
            # Create unique filename
            filename = f"article_{uuid.uuid4().hex[:8]}.jpg"
            image_file = ImageFile(BytesIO(response.content), name=filename)

            # Create Wagtail Image object
            cover_image = Image(
                title=f"Cover for {title[:50]}...",
                file=image_file
            )
            cover_image.save()
            return cover_image

    except Exception as e:
        print(f"Failed to download marketing image: {e}")

    return None


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
        "cover_image_url": "https://example.com/image.jpg" (optional - auto-generates if not provided),
        "api_key": "your-secret-api-key"
    }

    Features:
    - Automatic image generation from Unsplash based on category
    - Unique slug generation
    - SEO optimization (title, meta description)
    - Automatic publishing
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
        
        # Handle cover image - try provided URL first, then auto-generate
        cover_image = None
        cover_image_url = data.get('cover_image_url')

        if cover_image_url:
            # Try to use provided image URL
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
                print(f"Failed to download provided image: {e}")

        # If no image provided or download failed, get automatic marketing image
        if not cover_image:
            cover_image = get_marketing_image(title, category_slug)
        
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
