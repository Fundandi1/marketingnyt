"""
Management command to import articles from CSV or Markdown files.
"""

import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify
from wagtail.models import Site

from news.models import ArticlePage, Category, HomePage


class Command(BaseCommand):
    help = "Import articles from CSV or Markdown files"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to CSV or Markdown file"
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["csv", "markdown"],
            default="csv",
            help="File format (csv or markdown)"
        )
        parser.add_argument(
            "--category",
            type=str,
            help="Default category slug for articles"
        )
        parser.add_argument(
            "--author",
            type=str,
            default="Admin",
            help="Default author name"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be imported without actually importing"
        )
    
    def handle(self, *args, **options):
        file_path = options["file_path"]
        file_format = options["format"]
        category_slug = options["category"]
        default_author = options["author"]
        dry_run = options["dry_run"]
        
        if not os.path.exists(file_path):
            raise CommandError(f"File not found: {file_path}")
        
        # Get or create default category
        if category_slug:
            try:
                default_category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                raise CommandError(f"Category not found: {category_slug}")
        else:
            default_category, created = Category.objects.get_or_create(
                slug="general",
                defaults={"name": "General", "description": "General articles"}
            )
            if created:
                self.stdout.write(f"Created default category: {default_category.name}")
        
        # Get home page as parent
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page.specific
        
        if file_format == "csv":
            self.import_from_csv(file_path, home_page, default_category, default_author, dry_run)
        elif file_format == "markdown":
            self.import_from_markdown(file_path, home_page, default_category, default_author, dry_run)
    
    def import_from_csv(self, file_path, parent_page, default_category, default_author, dry_run):
        """Import articles from CSV file."""
        imported_count = 0
        
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                title = row.get("title", "").strip()
                if not title:
                    self.stdout.write(self.style.WARNING(f"Skipping row with empty title"))
                    continue
                
                slug = row.get("slug", "").strip() or slugify(title)
                summary = row.get("summary", "").strip()
                body_text = row.get("body", "").strip()
                author = row.get("author", "").strip() or default_author
                category_name = row.get("category", "").strip()
                
                # Get or create category
                if category_name:
                    category, created = Category.objects.get_or_create(
                        slug=slugify(category_name),
                        defaults={"name": category_name}
                    )
                else:
                    category = default_category
                
                # Parse published date
                published_str = row.get("published_at", "").strip()
                if published_str:
                    try:
                        published_at = datetime.strptime(published_str, "%Y-%m-%d %H:%M:%S")
                        published_at = timezone.make_aware(published_at)
                    except ValueError:
                        try:
                            published_at = datetime.strptime(published_str, "%Y-%m-%d")
                            published_at = timezone.make_aware(published_at)
                        except ValueError:
                            published_at = timezone.now()
                else:
                    published_at = timezone.now()
                
                if dry_run:
                    self.stdout.write(f"Would import: {title} (slug: {slug})")
                    continue
                
                # Check if article already exists
                if ArticlePage.objects.filter(slug=slug).exists():
                    self.stdout.write(self.style.WARNING(f"Article with slug '{slug}' already exists, skipping"))
                    continue
                
                # Create article
                article = ArticlePage(
                    title=title,
                    slug=slug,
                    summary=summary,
                    body=[("rich_text", body_text)] if body_text else [],
                    category=category,
                    author=author,
                    published_at=published_at,
                )
                
                parent_page.add_child(instance=article)
                article.save_revision().publish()
                
                imported_count += 1
                self.stdout.write(f"Imported: {title}")
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported {imported_count} articles")
            )
    
    def import_from_markdown(self, file_path, parent_page, default_category, default_author, dry_run):
        """Import articles from Markdown file."""
        # This is a simplified implementation
        # In a real scenario, you'd parse frontmatter and markdown content
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by markdown headers (this is very basic)
        articles = content.split("\n# ")
        
        imported_count = 0
        
        for i, article_content in enumerate(articles):
            if not article_content.strip():
                continue
            
            lines = article_content.strip().split("\n")
            title = lines[0].replace("# ", "").strip()
            
            if not title:
                continue
            
            slug = slugify(title)
            body_text = "\n".join(lines[1:]).strip()
            
            if dry_run:
                self.stdout.write(f"Would import: {title} (slug: {slug})")
                continue
            
            # Check if article already exists
            if ArticlePage.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f"Article with slug '{slug}' already exists, skipping"))
                continue
            
            # Create article
            article = ArticlePage(
                title=title,
                slug=slug,
                summary=body_text[:200] + "..." if len(body_text) > 200 else body_text,
                body=[("rich_text", body_text)] if body_text else [],
                category=default_category,
                author=default_author,
                published_at=timezone.now(),
            )
            
            parent_page.add_child(instance=article)
            article.save_revision().publish()
            
            imported_count += 1
            self.stdout.write(f"Imported: {title}")
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported {imported_count} articles")
            )
