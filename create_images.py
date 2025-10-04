#!/usr/bin/env python3
"""
Create high-quality placeholder images for MarketingNyt.dk articles.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

# Image configurations
IMAGES = [
    {
        "filename": "google-core-web-vitals.jpg",
        "title": "Google Core Web Vitals",
        "subtitle": "Performance Update 2024",
        "color": "#4285f4",
        "icon": "📊"
    },
    {
        "filename": "facebook-ads-strategies.jpg", 
        "title": "Facebook Ads",
        "subtitle": "5 Winning Strategies",
        "color": "#1877f2",
        "icon": "📱"
    },
    {
        "filename": "chatgpt-content-marketing.jpg",
        "title": "ChatGPT Marketing",
        "subtitle": "Complete Guide 2024",
        "color": "#10a37f",
        "icon": "🤖"
    },
    {
        "filename": "tiktok-ads-guide.jpg",
        "title": "TikTok Ads",
        "subtitle": "Beginner's Success Guide",
        "color": "#ff0050",
        "icon": "🎵"
    },
    {
        "filename": "local-seo-guide.jpg",
        "title": "Local SEO",
        "subtitle": "Dominate Local Search",
        "color": "#34a853",
        "icon": "📍"
    },
    {
        "filename": "marketing-automation.jpg",
        "title": "Marketing Automation",
        "subtitle": "ROI Guide 2024",
        "color": "#ea4335",
        "icon": "⚙️"
    }
]

def create_gradient_background(width, height, color1, color2):
    """Create a gradient background."""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Convert hex colors to RGB
    color1_rgb = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    color2_rgb = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    
    for y in range(height):
        ratio = y / height
        r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
        g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
        b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def darken_color(hex_color, factor=0.3):
    """Darken a hex color by a factor."""
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    darkened = tuple(int(c * (1 - factor)) for c in rgb)
    return '#' + ''.join(f'{c:02x}' for c in darkened)

def create_article_image(config, width=1200, height=630):
    """Create a professional article image."""
    # Create gradient background
    dark_color = darken_color(config["color"])
    image = create_gradient_background(width, height, config["color"], dark_color)
    draw = ImageDraw.Draw(image)
    
    # Add subtle pattern overlay
    overlay = Image.new('RGBA', (width, height), (255, 255, 255, 10))
    pattern_draw = ImageDraw.Draw(overlay)
    
    # Create dot pattern
    for x in range(0, width, 40):
        for y in range(0, height, 40):
            if (x + y) % 80 == 0:
                pattern_draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255, 30))
    
    image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        icon_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 120)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        icon_font = ImageFont.load_default()
    
    # Add icon
    icon_x = 100
    icon_y = 100
    draw.text((icon_x, icon_y), config["icon"], font=icon_font, fill="white")
    
    # Add title
    title_x = 100
    title_y = 280
    draw.text((title_x, title_y), config["title"], font=title_font, fill="white", stroke_width=2, stroke_fill="black")

    # Add subtitle
    subtitle_x = 100
    subtitle_y = 380
    draw.text((subtitle_x, subtitle_y), config["subtitle"], font=subtitle_font, fill=(255, 255, 255, 230), stroke_width=1, stroke_fill="black")

    # Add MarketingNyt.dk branding
    brand_text = "MarketingNyt.dk"
    brand_x = width - 300
    brand_y = height - 80
    draw.text((brand_x, brand_y), brand_text, font=subtitle_font, fill=(255, 255, 255, 180))
    
    return image

def create_logo():
    """Create a simple logo for the site."""
    width, height = 200, 60
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font = ImageFont.load_default()
    
    # Draw text
    text = "MarketingNyt.dk"
    draw.text((10, 20), text, font=font, fill="#e74c3c")
    
    return image

def main():
    """Create all images."""
    os.makedirs("media/original_images", exist_ok=True)
    
    print("Creating article images...")
    for config in IMAGES:
        print(f"Creating {config['filename']}...")
        image = create_article_image(config)
        image.save(f"media/original_images/{config['filename']}", "JPEG", quality=95)
    
    print("Creating logo...")
    logo = create_logo()
    logo.save("media/original_images/logo.png", "PNG")
    
    print("Creating default OG image...")
    default_config = {
        "title": "MarketingNyt.dk",
        "subtitle": "Danmarks Marketing Platform",
        "color": "#e74c3c",
        "icon": "📈"
    }
    og_image = create_article_image(default_config)
    og_image.save("media/original_images/default-og.jpg", "JPEG", quality=95)
    
    print("All images created successfully!")

if __name__ == "__main__":
    main()
