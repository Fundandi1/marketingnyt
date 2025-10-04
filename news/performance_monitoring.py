"""
Performance monitoring and optimization utilities for MarketingNyt.dk
"""

import time
import logging
from functools import wraps
from django.core.cache import cache, caches
from django.conf import settings
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, vary_on_headers
from django.views.decorators.gzip import gzip_page
from django.http import HttpResponse
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)


class PerformanceMiddleware:
    """
    Middleware to monitor and optimize performance.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        # Add performance headers
        response = self.get_response(request)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Add performance headers
        response['X-Response-Time'] = f'{response_time:.3f}s'
        response['X-DB-Queries'] = len(connection.queries)
        
        # Log slow requests
        if response_time > 1.0:  # Log requests slower than 1 second
            logger.warning(
                f'Slow request: {request.path} took {response_time:.3f}s '
                f'with {len(connection.queries)} DB queries'
            )
        
        # Add cache headers for static content
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        
        return response


def cache_page_per_user(timeout):
    """
    Cache decorator that varies by user authentication status.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            cache_key = f'page_{request.path}_{request.user.is_authenticated}'
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response
            
            # Generate response
            response = view_func(request, *args, **kwargs)
            
            # Cache the response
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


def cache_template_fragment(fragment_name, timeout=300):
    """
    Cache template fragments with automatic invalidation.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f'template_fragment_{fragment_name}_{hash(str(args) + str(kwargs))}'
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


class DatabaseOptimizer:
    """
    Database query optimization utilities.
    """
    
    @staticmethod
    def get_optimized_articles(limit=10, category=None):
        """
        Get articles with optimized queries using select_related and prefetch_related.
        """
        from .models import ArticlePage
        
        cache_key = f'optimized_articles_{limit}_{category}'
        cached_articles = caches['pages'].get(cache_key)
        
        if cached_articles is not None:
            return cached_articles
        
        queryset = ArticlePage.objects.live().public().select_related(
            'category'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')
        
        if category:
            queryset = queryset.filter(category=category)
        
        articles = list(queryset[:limit])
        
        # Cache for 30 minutes
        caches['pages'].set(cache_key, articles, 1800)
        
        return articles
    
    @staticmethod
    def get_popular_articles(limit=5):
        """
        Get popular articles based on view count or other metrics.
        """
        cache_key = f'popular_articles_{limit}'
        cached_articles = caches['pages'].get(cache_key)
        
        if cached_articles is not None:
            return cached_articles
        
        from .models import ArticlePage
        
        # For now, use recent articles as popular
        # In production, you might track view counts
        articles = list(
            ArticlePage.objects.live().public()
            .select_related('category')
            .order_by('-published_at')[:limit]
        )
        
        # Cache for 1 hour
        caches['pages'].set(cache_key, articles, 3600)
        
        return articles


class ImageOptimizer:
    """
    Image optimization and caching utilities.
    """
    
    @staticmethod
    def get_optimized_rendition(image, filter_spec, cache_timeout=3600):
        """
        Get image rendition with caching.
        """
        if not image:
            return None
        
        cache_key = f'image_rendition_{image.id}_{filter_spec}'
        cached_rendition = caches['images'].get(cache_key)
        
        if cached_rendition is not None:
            return cached_rendition
        
        try:
            rendition = image.get_rendition(filter_spec)
            caches['images'].set(cache_key, rendition, cache_timeout)
            return rendition
        except Exception as e:
            logger.error(f'Error generating image rendition: {e}')
            return None
    
    @staticmethod
    def preload_article_images(articles):
        """
        Preload images for a list of articles to reduce database queries.
        """
        image_ids = [
            article.cover_image.id for article in articles 
            if hasattr(article, 'cover_image') and article.cover_image
        ]
        
        if not image_ids:
            return
        
        from wagtail.images.models import Image
        
        # Preload images
        images = {
            img.id: img for img in 
            Image.objects.filter(id__in=image_ids)
        }
        
        # Attach images to articles to avoid additional queries
        for article in articles:
            if hasattr(article, 'cover_image') and article.cover_image:
                article._cached_cover_image = images.get(article.cover_image.id)


def performance_monitor(func):
    """
    Decorator to monitor function performance.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log slow functions
            if execution_time > 0.5:  # Log functions slower than 500ms
                logger.warning(
                    f'Slow function: {func.__name__} took {execution_time:.3f}s'
                )
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f'Function {func.__name__} failed after {execution_time:.3f}s: {e}'
            )
            raise
    
    return wrapper


class CacheInvalidator:
    """
    Utilities for intelligent cache invalidation.
    """
    
    @staticmethod
    def invalidate_article_caches(article):
        """
        Invalidate all caches related to an article.
        """
        # Invalidate article-specific caches
        cache_patterns = [
            f'page_{article.url}*',
            f'optimized_articles_*',
            f'popular_articles_*',
            f'template_fragment_*',
        ]
        
        for pattern in cache_patterns:
            cache.delete_pattern(pattern)
        
        # Invalidate category caches if article has category
        if hasattr(article, 'category') and article.category:
            cache.delete_pattern(f'optimized_articles_*_{article.category.id}')
    
    @staticmethod
    def invalidate_homepage_cache():
        """
        Invalidate homepage and related caches.
        """
        cache_patterns = [
            'page_/*',
            'optimized_articles_*',
            'popular_articles_*',
            'template_fragment_homepage_*',
        ]
        
        for pattern in cache_patterns:
            cache.delete_pattern(pattern)


# Performance decorators for views
def optimized_page_view(timeout=300):
    """
    Comprehensive optimization decorator for page views.
    """
    def decorator(view_func):
        # Apply multiple optimizations
        view_func = gzip_page(view_func)
        view_func = vary_on_headers('User-Agent', 'Accept-Encoding')(view_func)
        view_func = cache_page_per_user(timeout)(view_func)
        view_func = performance_monitor(view_func)
        
        return view_func
    return decorator


# Context processor for performance data
def performance_context(request):
    """
    Add performance-related context variables.
    """
    return {
        'cache_enabled': bool(getattr(settings, 'CACHES', {})),
        'debug_mode': settings.DEBUG,
        'performance_monitoring': True,
    }
