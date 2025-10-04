#!/usr/bin/env python3
"""
Verification script for MarketingNyt.dk setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

def verify_models():
    """Verify that all models can be imported and basic operations work."""
    print("🔍 Verifying models...")
    
    try:
        from news.models import HomePage, ArticlePage, Category, SiteSettings
        from wagtail.models import Site
        
        # Check if we can query models
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page.specific
        
        categories = Category.objects.all()
        articles = ArticlePage.objects.all()
        
        print(f"✅ Found {categories.count()} categories")
        print(f"✅ Found {articles.count()} articles")
        print(f"✅ Home page: {home_page.title}")
        
        return True
    except Exception as e:
        print(f"❌ Model verification failed: {e}")
        return False


def verify_templates():
    """Verify that templates exist and can be rendered."""
    print("\n🔍 Verifying templates...")
    
    required_templates = [
        'base.html',
        'news/home_page.html',
        'news/article_page.html',
        'news/category_page.html',
        '404.html',
        '500.html'
    ]
    
    templates_dir = Path('templates')
    missing_templates = []
    
    for template in required_templates:
        template_path = templates_dir / template
        if not template_path.exists():
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ Missing templates: {', '.join(missing_templates)}")
        return False
    else:
        print("✅ All required templates found")
        return True


def verify_static_files():
    """Verify that static files exist."""
    print("\n🔍 Verifying static files...")
    
    static_dir = Path('static')
    required_files = [
        'css/main.css',
        'js/main.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = static_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing static files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required static files found")
        return True


def verify_management_commands():
    """Verify that management commands work."""
    print("\n🔍 Verifying management commands...")
    
    try:
        from django.core.management import get_commands
        commands = get_commands()
        
        required_commands = [
            'create_sample_data',
            'import_articles',
            'suggest_internal_links'
        ]
        
        missing_commands = []
        for cmd in required_commands:
            if cmd not in commands:
                missing_commands.append(cmd)
        
        if missing_commands:
            print(f"❌ Missing commands: {', '.join(missing_commands)}")
            return False
        else:
            print("✅ All management commands available")
            return True
    except Exception as e:
        print(f"❌ Command verification failed: {e}")
        return False


def verify_urls():
    """Verify that URL patterns are configured correctly."""
    print("\n🔍 Verifying URL configuration...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test basic URLs
        test_urls = [
            ('/', 'Home page'),
            ('/robots.txt', 'Robots.txt'),
            ('/sitemap.xml', 'Sitemap'),
            ('/healthz', 'Health check'),
            ('/admin/', 'Wagtail admin')
        ]
        
        for url, description in test_urls:
            try:
                response = client.get(url)
                if response.status_code in [200, 302]:  # 302 for admin redirect
                    print(f"✅ {description}: {response.status_code}")
                else:
                    print(f"⚠️  {description}: {response.status_code}")
            except Exception as e:
                print(f"❌ {description}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ URL verification failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("🚀 Verifying MarketingNyt.dk setup...\n")
    
    checks = [
        verify_models,
        verify_templates,
        verify_static_files,
        verify_management_commands,
        verify_urls
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print(f"\n📊 Verification Results:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n🎉 All checks passed! Your MarketingNyt.dk setup is ready.")
        print("\nYou can now:")
        print("• Run 'make run' to start the development server")
        print("• Visit http://localhost:8000 to see your site")
        print("• Visit http://localhost:8000/admin/ for content management")
        return True
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
