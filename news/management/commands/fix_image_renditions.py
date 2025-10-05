"""
Management command to fix Wagtail image renditions and force regeneration.
"""

import os
from django.core.management.base import BaseCommand
from wagtail.images.models import Image, Rendition


class Command(BaseCommand):
    help = 'Fix Wagtail image renditions and force regeneration'

    def handle(self, *args, **options):
        self.stdout.write('Fixing image renditions...')
        
        # Delete all existing renditions to force regeneration
        rendition_count = Rendition.objects.count()
        self.stdout.write(f'Deleting {rendition_count} existing renditions...')
        Rendition.objects.all().delete()
        self.stdout.write('✅ All renditions deleted')
        
        # Get all images
        images = Image.objects.all()
        self.stdout.write(f'Found {images.count()} images to process')
        
        for image in images:
            try:
                self.stdout.write(f'Processing: {image.title}')
                self.stdout.write(f'  Current URL: {image.file.url}')
                
                # Force regeneration of common renditions
                try:
                    # Generate thumbnail
                    thumbnail = image.get_rendition('max-165x165')
                    self.stdout.write(f'  ✅ Thumbnail: {thumbnail.url}')
                    
                    # Generate medium size
                    medium = image.get_rendition('max-800x600')
                    self.stdout.write(f'  ✅ Medium: {medium.url}')
                    
                except Exception as e:
                    self.stdout.write(f'  ❌ Error generating renditions: {e}')
                    
            except Exception as e:
                self.stdout.write(f'❌ Error processing {image.title}: {e}')
        
        self.stdout.write('\n✅ Image rendition fix complete!')
        self.stdout.write('All image thumbnails should now be regenerated with correct Cloudinary URLs')
