"""
StreamField blocks for the news app.
"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class RichTextBlock(blocks.RichTextBlock):
    """Rich text block with custom features."""
    
    class Meta:
        icon = "doc-full"
        label = "Rich Text"
        template = "news/blocks/rich_text.html"


class HeadingBlock(blocks.StructBlock):
    """Heading block for H2/H3 headings."""
    level = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
        ],
        default="h2"
    )
    text = blocks.CharBlock(max_length=200)
    
    class Meta:
        icon = "title"
        label = "Heading"
        template = "news/blocks/heading.html"


class QuoteBlock(blocks.StructBlock):
    """Quote block for pull quotes."""
    quote = blocks.TextBlock()
    attribution = blocks.CharBlock(max_length=100, required=False)
    
    class Meta:
        icon = "openquote"
        label = "Quote"
        template = "news/blocks/quote.html"


class ImageBlock(blocks.StructBlock):
    """Image block with caption."""
    image = ImageChooserBlock()
    caption = blocks.CharBlock(max_length=200, required=False)
    alt_text = blocks.CharBlock(
        max_length=200,
        required=False,
        help_text="Alternative text for screen readers"
    )
    
    class Meta:
        icon = "image"
        label = "Image"
        template = "news/blocks/image.html"


class CalloutBlock(blocks.StructBlock):
    """Callout block for highlighted information."""
    title = blocks.CharBlock(max_length=100, required=False)
    text = blocks.RichTextBlock()
    style = blocks.ChoiceBlock(
        choices=[
            ("info", "Info"),
            ("warning", "Warning"),
            ("success", "Success"),
            ("error", "Error"),
        ],
        default="info"
    )
    
    class Meta:
        icon = "help"
        label = "Callout"
        template = "news/blocks/callout.html"


class FAQBlock(blocks.StructBlock):
    """FAQ block for frequently asked questions."""
    question = blocks.CharBlock(max_length=200)
    answer = blocks.RichTextBlock()
    
    class Meta:
        icon = "help"
        label = "FAQ Item"
        template = "news/blocks/faq.html"


class FAQListBlock(blocks.StructBlock):
    """FAQ list block containing multiple FAQ items."""
    title = blocks.CharBlock(max_length=100, default="Ofte stillede spørgsmål")
    faqs = blocks.ListBlock(FAQBlock())
    
    class Meta:
        icon = "list-ul"
        label = "FAQ List"
        template = "news/blocks/faq_list.html"


class ArticleStreamBlock(blocks.StreamBlock):
    """Main StreamBlock for article content."""
    rich_text = RichTextBlock()
    heading = HeadingBlock()
    quote = QuoteBlock()
    image = ImageBlock()
    callout = CalloutBlock()
    faq_list = FAQListBlock()
    
    class Meta:
        block_counts = {
            "rich_text": {"max_num": 20},
            "heading": {"max_num": 10},
            "quote": {"max_num": 5},
            "image": {"max_num": 10},
            "callout": {"max_num": 5},
            "faq_list": {"max_num": 3},
        }
