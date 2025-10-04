"""
Management command to suggest internal links between articles.
"""

import re
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.db.models import Q

from news.models import ArticlePage


class Command(BaseCommand):
    help = "Suggest internal links between articles based on keywords and tags"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--min-score",
            type=float,
            default=0.3,
            help="Minimum similarity score (0.0-1.0)"
        )
        parser.add_argument(
            "--max-suggestions",
            type=int,
            default=5,
            help="Maximum suggestions per article"
        )
        parser.add_argument(
            "--output-format",
            type=str,
            choices=["text", "csv"],
            default="text",
            help="Output format"
        )
    
    def handle(self, *args, **options):
        min_score = options["min_score"]
        max_suggestions = options["max_suggestions"]
        output_format = options["output_format"]
        
        articles = ArticlePage.objects.live().select_related("category").prefetch_related("tags")
        
        if output_format == "csv":
            self.stdout.write("source_title,source_url,target_title,target_url,score,reason")
        
        for article in articles:
            suggestions = self.get_suggestions(article, articles, min_score, max_suggestions)
            
            if output_format == "text":
                if suggestions:
                    self.stdout.write(f"\n{article.title}")
                    self.stdout.write("-" * len(article.title))
                    for suggestion in suggestions:
                        self.stdout.write(f"  → {suggestion['title']} (score: {suggestion['score']:.2f}) - {suggestion['reason']}")
                        self.stdout.write(f"    URL: {suggestion['url']}")
            else:  # csv
                for suggestion in suggestions:
                    self.stdout.write(
                        f'"{article.title}","{article.get_full_url()}","'
                        f'{suggestion["title"]}","{suggestion["url"]}",'
                        f'{suggestion["score"]:.2f},"{suggestion["reason"]}"'
                    )
    
    def get_suggestions(self, source_article, all_articles, min_score, max_suggestions):
        """Get link suggestions for an article."""
        suggestions = []
        
        # Extract keywords from title and summary
        source_keywords = self.extract_keywords(source_article.title + " " + source_article.summary)
        source_tags = set(tag.name.lower() for tag in source_article.tags.all())
        
        for target_article in all_articles:
            if target_article.id == source_article.id:
                continue
            
            score = 0.0
            reasons = []
            
            # Same category bonus
            if target_article.category_id == source_article.category_id:
                score += 0.3
                reasons.append("same category")
            
            # Tag overlap
            target_tags = set(tag.name.lower() for tag in target_article.tags.all())
            tag_overlap = len(source_tags & target_tags)
            if tag_overlap > 0:
                tag_score = min(tag_overlap * 0.2, 0.4)
                score += tag_score
                reasons.append(f"{tag_overlap} shared tags")
            
            # Keyword overlap
            target_keywords = self.extract_keywords(target_article.title + " " + target_article.summary)
            keyword_overlap = len(source_keywords & target_keywords)
            if keyword_overlap > 0:
                keyword_score = min(keyword_overlap * 0.1, 0.3)
                score += keyword_score
                reasons.append(f"{keyword_overlap} shared keywords")
            
            # Title similarity
            title_similarity = self.calculate_title_similarity(source_article.title, target_article.title)
            if title_similarity > 0.2:
                score += title_similarity * 0.2
                reasons.append("similar title")
            
            if score >= min_score:
                suggestions.append({
                    "title": target_article.title,
                    "url": target_article.get_full_url(),
                    "score": score,
                    "reason": ", ".join(reasons)
                })
        
        # Sort by score and limit
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions[:max_suggestions]
    
    def extract_keywords(self, text):
        """Extract keywords from text."""
        # Simple keyword extraction - remove common words
        stop_words = {
            "og", "i", "på", "til", "af", "for", "med", "er", "det", "en", "et", "den",
            "de", "som", "at", "har", "kan", "vil", "skal", "var", "blev", "bliver",
            "and", "the", "a", "an", "in", "on", "at", "to", "for", "of", "with",
            "is", "are", "was", "were", "be", "been", "have", "has", "had", "do",
            "does", "did", "will", "would", "could", "should", "may", "might"
        }
        
        # Extract words (3+ characters, not stop words)
        words = re.findall(r'\b[a-zA-ZæøåÆØÅ]{3,}\b', text.lower())
        keywords = set(word for word in words if word not in stop_words)
        
        return keywords
    
    def calculate_title_similarity(self, title1, title2):
        """Calculate similarity between two titles."""
        words1 = set(re.findall(r'\b[a-zA-ZæøåÆØÅ]{3,}\b', title1.lower()))
        words2 = set(re.findall(r'\b[a-zA-ZæøåÆØÅ]{3,}\b', title2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
