"""
Management command to replace all images with working Cloudinary samples.
"""

import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from wagtail.images.models import Image, Rendition


class Command(BaseCommand):
    help = 'Replace all images with working Cloudinary samples'

    def handle(self, *args, **options):
        self.stdout.write('Replacing images with Cloudinary samples...')
        
        # Delete all existing renditions first
        Rendition.objects.all().delete()
        self.stdout.write('✅ Deleted all renditions')
        
        # Sample images from Cloudinary's public samples
        sample_images = {
            'Marketing Strategy': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg',
            'Digital Marketing': 'https://res.cloudinary.com/demo/image/upload/v1571218039/samples/people/kitchen-bar.jpg',
            'Content Marketing': 'https://res.cloudinary.com/demo/image/upload/v1571218039/samples/landscapes/nature-mountains.jpg',
            'Social Media': 'https://res.cloudinary.com/demo/image/upload/v1571218039/samples/people/bicycle.jpg'
        }
        
        # Get all images
        images = Image.objects.all()
        self.stdout.write(f'Found {images.count()} images to replace')
        
        replaced = 0
        
        for i, image in enumerate(images):
            try:
                # Get a sample image URL
                sample_titles = list(sample_images.keys())
                sample_title = sample_titles[i % len(sample_titles)]
                sample_url = sample_images[sample_title]
                
                self.stdout.write(f'Replacing: {image.title} with {sample_title}')
                
                # Download the sample image
                response = requests.get(sample_url, timeout=10)
                if response.status_code == 200:
                    # Create new file
                    file_name = f"{sample_title.lower().replace(' ', '_')}.jpg"
                    new_file = ContentFile(response.content, name=file_name)
                    
                    # Update the image
                    image.title = sample_title
                    image.file.save(file_name, new_file, save=False)
                    image.save()
                    
                    self.stdout.write(f'✅ Replaced with: {image.file.url}')
                    replaced += 1
                    
                    # Test rendition generation
                    try:
                        thumbnail = image.get_rendition('max-165x165')
                        self.stdout.write(f'  ✅ Thumbnail generated: {thumbnail.url}')
                    except Exception as e:
                        self.stdout.write(f'  ⚠️  Thumbnail generation failed: {e}')
                        
                else:
                    self.stdout.write(f'❌ Failed to download sample for {image.title}')
                    
            except Exception as e:
                self.stdout.write(f'❌ Error replacing {image.title}: {e}')
        
        self.stdout.write(f'\n✅ Replacement complete!')
        self.stdout.write(f'Successfully replaced: {replaced} images')
        self.stdout.write('All images should now work with Cloudinary URLs!')
