"""
Models for the news app.
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import ArticleStreamBlock


@register_snippet
class Video(models.Model):
    """Video model for uploading and managing videos."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('file'),
        FieldPanel('thumbnail'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['-created_at']


class ArticlePageTag(TaggedItemBase):
    """Tag model for ArticlePage."""
    content_object = ParentalKey(
        "ArticlePage",
        related_name="tagged_items",
        on_delete=models.CASCADE
    )


@register_snippet
class Category(models.Model):
    """Category snippet for organizing articles."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
    ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categories"


@register_snippet
class SiteSettings(models.Model):
    """Global site settings."""
    site_name = models.CharField(max_length=100, default="MarketingNyt.dk")
    default_meta_title = models.CharField(max_length=60, blank=True)
    default_meta_description = models.TextField(max_length=160, blank=True)
    social_twitter = models.CharField(max_length=100, blank=True)
    social_facebook = models.CharField(max_length=100, blank=True)
    social_linkedin = models.CharField(max_length=100, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    default_og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("site_name"),
            FieldPanel("logo"),
        ], heading="Site Identity"),
        MultiFieldPanel([
            FieldPanel("default_meta_title"),
            FieldPanel("default_meta_description"),
            FieldPanel("default_og_image"),
        ], heading="Default SEO"),
        MultiFieldPanel([
            FieldPanel("social_twitter"),
            FieldPanel("social_facebook"),
            FieldPanel("social_linkedin"),
        ], heading="Social Media"),
    ]
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class BasicPage(Page):
    """Basic page model for simple content pages like About, Contact, etc."""
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Basic Page"


class HomePage(Page):
    """Home page model."""
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_image"),
        ], heading="Hero Section"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get ALL articles ordered by newest first (no featured system)
        # Exclude Podcasts category - those should only appear in Podcasts section
        # This ensures new articles always appear at the top
        podcast_category = Category.objects.filter(slug='podcasts').first()
        latest_articles_query = ArticlePage.objects.live()

        if podcast_category:
            latest_articles_query = latest_articles_query.exclude(category=podcast_category)

        latest_articles = latest_articles_query.order_by("-published_at")[:100]

        # Get categories
        categories = Category.objects.all()

        context.update({
            "latest_articles": latest_articles,
            "categories": categories,
        })
        return context


class CategoryPage(Page):
    """Category page model."""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="pages"
    )
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("intro"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get articles in this category
        articles = ArticlePage.objects.live().filter(
            category=self.category
        ).order_by("-published_at")
        
        # Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(articles, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        context.update({
            "articles": page_obj,
            "category": self.category,
        })
        return context


class ArticlePage(Page):
    """Article page model."""
    summary = models.TextField(
        max_length=300,
        help_text="Brief summary for meta description and previews"
    )
    body = StreamField(ArticleStreamBlock(), use_json_field=True)
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Cover image for the article (use either image or video, not both)"
    )
    cover_video = models.ForeignKey(
        Video,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Cover video for the article. If set, this will be used instead of cover image."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles"
    )
    author = models.CharField(max_length=100)
    published_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="External URL to redirect to (e.g. for podcasts)"
    )
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("cover_image"),
        FieldPanel("cover_video"),
        FieldPanel("category"),
        FieldPanel("author"),
        FieldPanel("published_at"),
        FieldPanel("is_featured"),
        FieldPanel("external_url"),
        FieldPanel("tags"),
        FieldPanel("body"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
        index.SearchField("author"),
        index.FilterField("category"),
        index.FilterField("published_at"),
    ]
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if empty
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_context(self, request):
        context = super().get_context(request)

        # Exclude podcast category from related articles
        podcast_category = Category.objects.filter(slug='podcasts').first()

        # Get related articles from same category (excluding podcasts and current article)
        related_query = ArticlePage.objects.live().filter(
            category=self.category
        ).exclude(id=self.id)

        if podcast_category:
            related_query = related_query.exclude(category=podcast_category)

        related_articles = list(related_query.order_by("-published_at")[:3])

        # If not enough related by category, get from other categories (excluding podcasts)
        if len(related_articles) < 3:
            # Get articles from other categories (not podcasts, not current category, not current article)
            additional_query = ArticlePage.objects.live().exclude(id=self.id)

            if podcast_category:
                additional_query = additional_query.exclude(category=podcast_category)

            # Exclude current category and already selected articles
            additional_query = additional_query.exclude(category=self.category)
            if related_articles:
                additional_query = additional_query.exclude(
                    id__in=[art.id for art in related_articles]
                )

            additional_related = list(additional_query.order_by("-published_at")[:3 - len(related_articles)])
            related_articles = related_articles + additional_related

        context.update({
            "related_articles": related_articles,
        })
        return context
    
    class Meta:
        ordering = ["-published_at"]


class RelatedArticle(Orderable):
    """Related articles for ArticlePage."""
    page = ParentalKey(ArticlePage, on_delete=models.CASCADE, related_name="related_articles")
    related_page = models.ForeignKey(
        ArticlePage,
        on_delete=models.CASCADE,
        related_name="+"
    )
    
    panels = [
        FieldPanel("related_page"),
    ]
