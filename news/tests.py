"""
Tests for the news app.
"""

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Site
from wagtail.test.utils import WagtailPageTestCase

from .models import ArticlePage, Category, HomePage, SiteSettings


class NewsModelsTestCase(TestCase):
    """Test cases for news models."""
    
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.home_page = self.site.root_page.specific
        
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test category description"
        )
    
    def test_category_creation(self):
        """Test category creation and string representation."""
        self.assertEqual(str(self.category), "Test Category")
        self.assertEqual(self.category.slug, "test-category")
    
    def test_category_auto_slug(self):
        """Test automatic slug generation for categories."""
        category = Category.objects.create(name="Auto Slug Test")
        self.assertEqual(category.slug, "auto-slug-test")
    
    def test_article_creation(self):
        """Test article page creation."""
        article = ArticlePage(
            title="Test Article",
            slug="test-article",
            summary="Test article summary",
            body=[("rich_text", "<p>Test content</p>")],
            category=self.category,
            author="Test Author",
            published_at=timezone.now()
        )
        
        self.home_page.add_child(instance=article)
        article.save_revision().publish()
        
        self.assertEqual(str(article), "Test Article")
        self.assertEqual(article.category, self.category)
        self.assertTrue(article.live)
    
    def test_article_auto_slug(self):
        """Test automatic slug generation for articles."""
        article = ArticlePage(
            title="Auto Slug Test Article",
            summary="Test summary",
            body=[],
            category=self.category,
            author="Test Author"
        )
        
        self.home_page.add_child(instance=article)
        self.assertEqual(article.slug, "auto-slug-test-article")


class NewsViewsTestCase(TestCase):
    """Test cases for news views."""
    
    def setUp(self):
        self.client = Client()
        self.site = Site.objects.get(is_default_site=True)
        self.home_page = self.site.root_page.specific
        
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        self.article = ArticlePage(
            title="Test Article",
            slug="test-article",
            summary="Test article summary",
            body=[("rich_text", "<p>Test content</p>")],
            category=self.category,
            author="Test Author",
            published_at=timezone.now()
        )
        
        self.home_page.add_child(instance=self.article)
        self.article.save_revision().publish()
    
    def test_robots_txt(self):
        """Test robots.txt view."""
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertIn("User-agent: *", response.content.decode())
        self.assertIn("Sitemap:", response.content.decode())
    
    def test_sitemap_index(self):
        """Test sitemap index view."""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
    
    def test_rss_feed(self):
        """Test RSS feed view."""
        response = self.client.get("/feed.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
        self.assertIn(self.article.title, response.content.decode())
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")


class SEOTestCase(TestCase):
    """Test cases for SEO functionality."""
    
    def setUp(self):
        self.client = Client()
        self.site = Site.objects.get(is_default_site=True)
        self.home_page = self.site.root_page.specific
        
        self.site_settings = SiteSettings.objects.create(
            site_name="Test Site",
            default_meta_title="Test Meta Title",
            default_meta_description="Test meta description"
        )
        
        self.category = Category.objects.create(
            name="SEO Category",
            slug="seo-category"
        )
        
        self.article = ArticlePage(
            title="SEO Test Article",
            slug="seo-test-article",
            summary="SEO test article summary for meta description",
            body=[
                ("heading", {"level": "h2", "text": "Test Heading"}),
                ("rich_text", "<p>Test content with <strong>keywords</strong></p>")
            ],
            category=self.category,
            author="SEO Author",
            published_at=timezone.now()
        )
        
        self.home_page.add_child(instance=self.article)
        self.article.save_revision().publish()
    
    def test_article_meta_tags(self):
        """Test that article pages have proper meta tags."""
        response = self.client.get(self.article.get_url())
        content = response.content.decode()
        
        # Check title tag
        self.assertIn(f"<title>{self.article.title}", content)
        
        # Check meta description
        self.assertIn(f'<meta name="description" content="{self.article.summary}"', content)
        
        # Check canonical tag
        self.assertIn('<link rel="canonical"', content)
        
        # Check OpenGraph tags
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:description"', content)
        self.assertIn('property="og:type" content="article"', content)
    
    def test_json_ld_structured_data(self):
        """Test JSON-LD structured data on article pages."""
        response = self.client.get(self.article.get_url())
        content = response.content.decode()
        
        # Check for JSON-LD script tags
        self.assertIn('application/ld+json', content)
        self.assertIn('"@type": "NewsArticle"', content)
        self.assertIn('"@type": "BreadcrumbList"', content)
    
    def test_sitemap_contains_articles(self):
        """Test that sitemap contains published articles."""
        response = self.client.get("/sitemap.xml")
        content = response.content.decode()
        
        # Should contain reference to article sitemap
        self.assertIn("articles", content)


class TemplateTagsTestCase(TestCase):
    """Test cases for template tags."""
    
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.home_page = self.site.root_page.specific
        
        self.category = Category.objects.create(
            name="Template Category",
            slug="template-category"
        )
        
        self.article = ArticlePage(
            title="Template Test Article",
            slug="template-test-article",
            summary="Template test summary",
            body=[
                ("heading", {"level": "h2", "text": "First Heading"}),
                ("rich_text", "<p>Some content</p>"),
                ("heading", {"level": "h3", "text": "Sub Heading"}),
                ("rich_text", "<p>More content</p>")
            ],
            category=self.category,
            author="Template Author",
            published_at=timezone.now()
        )
        
        self.home_page.add_child(instance=self.article)
        self.article.save_revision().publish()
    
    def test_table_of_contents_generation(self):
        """Test table of contents generation from StreamField."""
        from news.templatetags.news_tags import table_of_contents
        
        toc_html = table_of_contents(self.article.body)
        
        self.assertIn("table-of-contents", toc_html)
        self.assertIn("First Heading", toc_html)
        self.assertIn("Sub Heading", toc_html)
        self.assertIn("toc-h2", toc_html)
        self.assertIn("toc-h3", toc_html)
    
    def test_breadcrumbs_generation(self):
        """Test breadcrumbs generation."""
        from news.templatetags.news_tags import breadcrumbs
        
        breadcrumb_list = breadcrumbs(self.article)
        
        self.assertIsInstance(breadcrumb_list, list)
        self.assertTrue(len(breadcrumb_list) > 0)
    
    def test_json_ld_article_generation(self):
        """Test JSON-LD article data generation."""
        from news.templatetags.news_tags import json_ld_article
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get(self.article.get_url())
        
        json_data = json_ld_article(self.article, request)
        
        self.assertEqual(json_data["@type"], "NewsArticle")
        self.assertEqual(json_data["headline"], self.article.title)
        self.assertEqual(json_data["description"], self.article.summary)
        self.assertIn("author", json_data)
        self.assertIn("publisher", json_data)


class PerformanceTestCase(TestCase):
    """Test cases for performance features."""
    
    def setUp(self):
        self.client = Client()
    
    def test_cache_headers(self):
        """Test that appropriate cache headers are set."""
        response = self.client.get("/")
        
        # Check that response can be cached
        self.assertNotIn("no-cache", response.get("Cache-Control", ""))
    
    def test_static_files_compression(self):
        """Test that static files are properly configured."""
        # This would test Whitenoise configuration in a real deployment
        pass


class AccessibilityTestCase(TestCase):
    """Test cases for accessibility features."""
    
    def setUp(self):
        self.client = Client()
        self.site = Site.objects.get(is_default_site=True)
        self.home_page = self.site.root_page.specific
    
    def test_semantic_html(self):
        """Test that pages use semantic HTML elements."""
        response = self.client.get("/")
        content = response.content.decode()
        
        # Check for semantic elements
        self.assertIn("<header", content)
        self.assertIn("<main", content)
        self.assertIn("<nav", content)
        self.assertIn("<footer", content)
    
    def test_alt_text_on_images(self):
        """Test that images have alt text."""
        # This would be tested with actual image content
        pass
    
    def test_aria_labels(self):
        """Test that interactive elements have proper ARIA labels."""
        response = self.client.get("/")
        content = response.content.decode()
        
        # Check for ARIA labels on buttons
        self.assertIn('aria-label="Søg"', content)
        self.assertIn('aria-label="Menu"', content)
