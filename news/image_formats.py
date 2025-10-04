"""
Advanced image format handling for optimal performance.
Supports WebP, AVIF, and responsive images.
"""

from wagtail.images.formats import Format, register_image_format, unregister_image_format
from wagtail.images.models import AbstractImage, AbstractRendition
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ResponsiveImageFormat(Format):
    """
    Custom image format that generates responsive images with multiple formats.
    """
    
    def __init__(self, name, label, classnames=None, filter_spec=None):
        super().__init__(name, label, classnames, filter_spec)
    
    def image_to_html(self, image, alt_text, extra_attributes=None):
        """
        Generate responsive image HTML with WebP support and lazy loading.
        """
        if not image:
            return ''
        
        # Generate different sizes for responsive images
        sizes = [
            ('small', 'width-400'),
            ('medium', 'width-800'),
            ('large', 'width-1200'),
            ('xlarge', 'width-1600')
        ]
        
        # Generate WebP and fallback versions
        webp_sources = []
        jpg_sources = []
        
        for size_name, filter_spec in sizes:
            try:
                # Try to generate WebP version
                webp_rendition = image.get_rendition(f'{filter_spec}|format-webp')
                webp_sources.append(f'{webp_rendition.url} {webp_rendition.width}w')
            except:
                pass
            
            try:
                # Generate JPEG fallback
                jpg_rendition = image.get_rendition(filter_spec)
                jpg_sources.append(f'{jpg_rendition.url} {jpg_rendition.width}w')
            except:
                pass
        
        # Get default rendition for fallback
        try:
            default_rendition = image.get_rendition(self.filter_spec or 'width-800')
        except:
            return ''
        
        # Build responsive image HTML
        picture_html = ['<picture>']
        
        # WebP sources
        if webp_sources:
            picture_html.append(
                f'<source type="image/webp" srcset="{", ".join(webp_sources)}" '
                f'sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw">'
            )
        
        # JPEG sources
        if jpg_sources:
            picture_html.append(
                f'<source type="image/jpeg" srcset="{", ".join(jpg_sources)}" '
                f'sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw">'
            )
        
        # Fallback img tag
        img_attrs = {
            'src': default_rendition.url,
            'alt': alt_text or '',
            'width': default_rendition.width,
            'height': default_rendition.height,
            'loading': 'lazy',
            'decoding': 'async',
        }
        
        if self.classnames:
            img_attrs['class'] = self.classnames
        
        if extra_attributes:
            img_attrs.update(extra_attributes)
        
        img_html = '<img ' + ' '.join(f'{k}="{v}"' for k, v in img_attrs.items()) + '>'
        picture_html.append(img_html)
        picture_html.append('</picture>')
        
        return mark_safe(''.join(picture_html))


class LazyImageFormat(Format):
    """
    Image format with lazy loading and intersection observer support.
    """
    
    def image_to_html(self, image, alt_text, extra_attributes=None):
        if not image:
            return ''
        
        try:
            rendition = image.get_rendition(self.filter_spec or 'width-800')
        except:
            return ''
        
        # Create placeholder (low quality image placeholder)
        try:
            placeholder = image.get_rendition('width-50|jpegquality-20')
            placeholder_src = placeholder.url
        except:
            placeholder_src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PC9zdmc+'
        
        img_attrs = {
            'src': placeholder_src,
            'data-src': rendition.url,
            'alt': alt_text or '',
            'width': rendition.width,
            'height': rendition.height,
            'loading': 'lazy',
            'decoding': 'async',
            'class': f'lazy-image {self.classnames or ""}'.strip(),
        }
        
        if extra_attributes:
            img_attrs.update(extra_attributes)
        
        img_html = '<img ' + ' '.join(f'{k}="{v}"' for k, v in img_attrs.items()) + '>'
        
        return mark_safe(img_html)


# Register custom formats
def register_custom_formats():
    """Register all custom image formats."""
    
    # Unregister default formats we want to replace
    try:
        unregister_image_format('fullwidth')
        unregister_image_format('left')
        unregister_image_format('right')
    except:
        pass
    
    # Register responsive formats
    register_image_format(ResponsiveImageFormat(
        'responsive_fullwidth', 
        'Full width responsive', 
        'img-responsive img-fullwidth', 
        'width-1200'
    ))
    
    register_image_format(ResponsiveImageFormat(
        'responsive_half', 
        'Half width responsive', 
        'img-responsive img-half', 
        'width-600'
    ))
    
    register_image_format(LazyImageFormat(
        'lazy_fullwidth', 
        'Full width lazy', 
        'img-lazy img-fullwidth', 
        'width-1200'
    ))
    
    register_image_format(LazyImageFormat(
        'lazy_half', 
        'Half width lazy', 
        'img-lazy img-half', 
        'width-600'
    ))
    
    # Hero image format
    register_image_format(ResponsiveImageFormat(
        'hero', 
        'Hero image', 
        'img-hero', 
        'fill-1200x600'
    ))
    
    # Article cover format
    register_image_format(ResponsiveImageFormat(
        'article_cover', 
        'Article cover', 
        'img-article-cover', 
        'fill-800x400'
    ))
    
    # Thumbnail formats
    register_image_format(LazyImageFormat(
        'thumbnail', 
        'Thumbnail', 
        'img-thumbnail', 
        'fill-300x200'
    ))
    
    register_image_format(LazyImageFormat(
        'thumbnail_small', 
        'Small thumbnail', 
        'img-thumbnail-small', 
        'fill-150x100'
    ))


# Auto-register formats when module is imported
register_custom_formats()


def get_optimized_image_html(image, format_name='responsive_fullwidth', alt_text='', **kwargs):
    """
    Helper function to get optimized image HTML.
    """
    from wagtail.images.formats import get_image_format
    
    try:
        image_format = get_image_format(format_name)
        return image_format.image_to_html(image, alt_text, kwargs)
    except:
        # Fallback to basic image
        if image:
            try:
                rendition = image.get_rendition('width-800')
                return format_html(
                    '<img src="{}" alt="{}" loading="lazy" decoding="async">',
                    rendition.url,
                    alt_text
                )
            except:
                pass
        return ''
