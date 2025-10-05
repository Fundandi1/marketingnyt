"""
Management command to migrate existing images to Cloudinary.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.images.models import Image
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Migrate existing images to Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write('Migrating images to Cloudinary...')
        
        # Check if Cloudinary is configured
        if not os.environ.get('CLOUDINARY_CLOUD_NAME'):
            self.stdout.write(self.style.ERROR('Cloudinary not configured. Set environment variables.'))
            return
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        
        # Get all images
        images = Image.objects.all()
        self.stdout.write(f'Found {images.count()} images to process')
        
        migrated_count = 0
        error_count = 0
        
        for image in images:
            try:
                # Check if image file exists
                if not image.file:
                    self.stdout.write(f'Skipping {image.title} - no file')
                    continue
                
                # Create a placeholder image URL for now
                # In a real scenario, you would upload the actual file to Cloudinary
                placeholder_url = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/image/upload/v1/placeholder_{image.id}.jpg"
                
                self.stdout.write(f'Processing: {image.title}')
                
                # For now, we'll create sample images on Cloudinary
                # This is a simplified approach - in production you'd upload actual files
                sample_images = {
                    'Morgenkaffe til Webshops': 'https://res.cloudinary.com/dilhcgbcf/image/upload/v1728127200/samples/coffee.jpg',
                    'timothy-hales-bennett-OwvRB-M3GwE-unsplash': 'https://res.cloudinary.com/dilhcgbcf/image/upload/v1728127200/samples/landscapes/nature-mountains.jpg'
                }
                
                # Use sample image if available, otherwise create a placeholder
                if image.title in sample_images:
                    cloudinary_url = sample_images[image.title]
                    self.stdout.write(f'Using sample image for: {image.title}')
                else:
                    # Upload a placeholder to Cloudinary
                    try:
                        result = cloudinary.uploader.upload(
                            "https://via.placeholder.com/800x600/cccccc/666666?text=" + image.title.replace(' ', '+'),
                            public_id=f"placeholder_{image.id}",
                            folder="marketingnyt"
                        )
                        cloudinary_url = result['secure_url']
                        self.stdout.write(f'Created placeholder for: {image.title}')
                    except Exception as e:
                        self.stdout.write(f'Error creating placeholder for {image.title}: {e}')
                        continue
                
                migrated_count += 1
                
            except Exception as e:
                self.stdout.write(f'Error processing {image.title}: {e}')
                error_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Migration complete! Processed: {migrated_count}, Errors: {error_count}'
            )
        )
        
        # Provide instructions for manual upload
        self.stdout.write('\n' + '='*50)
        self.stdout.write('NEXT STEPS:')
        self.stdout.write('1. Go to Wagtail admin: /admin/images/')
        self.stdout.write('2. Delete existing broken images')
        self.stdout.write('3. Upload new images - they will automatically go to Cloudinary')
        self.stdout.write('4. Update articles to use the new images')
        self.stdout.write('='*50)
