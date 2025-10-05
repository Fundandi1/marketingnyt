"""
Management command to debug Django storage configuration.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage


class Command(BaseCommand):
    help = 'Debug Django storage configuration'

    def handle(self, *args, **options):
        self.stdout.write('Debugging storage configuration...')
        
        # Check environment variables
        self.stdout.write('\n=== ENVIRONMENT VARIABLES ===')
        self.stdout.write(f'CLOUDINARY_CLOUD_NAME: {os.environ.get("CLOUDINARY_CLOUD_NAME")}')
        self.stdout.write(f'CLOUDINARY_API_KEY: {os.environ.get("CLOUDINARY_API_KEY")}')
        self.stdout.write(f'CLOUDINARY_API_SECRET: {"*" * 20 if os.environ.get("CLOUDINARY_API_SECRET") else "Not set"}')
        
        # Check Django settings
        self.stdout.write('\n=== DJANGO SETTINGS ===')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {getattr(settings, "DEFAULT_FILE_STORAGE", "Not set")}')
        self.stdout.write(f'WAGTAILIMAGES_IMAGE_FILE_STORAGE: {getattr(settings, "WAGTAILIMAGES_IMAGE_FILE_STORAGE", "Not set")}')
        self.stdout.write(f'WAGTAILDOCS_DOCUMENT_FILE_STORAGE: {getattr(settings, "WAGTAILDOCS_DOCUMENT_FILE_STORAGE", "Not set")}')
        
        # Check actual storage being used
        self.stdout.write('\n=== ACTUAL STORAGE ===')
        self.stdout.write(f'default_storage class: {default_storage.__class__}')
        self.stdout.write(f'default_storage location: {getattr(default_storage, "location", "N/A")}')
        
        # Test storage
        self.stdout.write('\n=== STORAGE TEST ===')
        try:
            test_content = b'Hello Cloudinary Test'
            test_name = 'test_storage.txt'
            
            # Save test file
            saved_name = default_storage.save(test_name, test_content)
            self.stdout.write(f'✅ Saved test file: {saved_name}')
            
            # Get URL
            url = default_storage.url(saved_name)
            self.stdout.write(f'✅ File URL: {url}')
            
            # Check if it's Cloudinary
            if 'cloudinary.com' in url:
                self.stdout.write('✅ Using Cloudinary storage!')
            else:
                self.stdout.write('❌ NOT using Cloudinary storage!')
            
            # Clean up
            default_storage.delete(saved_name)
            self.stdout.write('✅ Test file cleaned up')
            
        except Exception as e:
            self.stdout.write(f'❌ Storage test failed: {e}')
        
        # Check Wagtail image storage specifically
        self.stdout.write('\n=== WAGTAIL IMAGE STORAGE ===')
        try:
            from wagtail.images.models import Image
            from django.core.files.base import ContentFile
            
            # Create a test image
            test_image = Image(title="Storage Test")
            test_content = ContentFile(b'fake image content', name='test.jpg')
            
            # Check what storage it would use
            storage = test_image.file.storage
            self.stdout.write(f'Wagtail Image storage class: {storage.__class__}')
            
            if hasattr(storage, 'cloud_name'):
                self.stdout.write(f'✅ Cloudinary cloud name: {storage.cloud_name}')
            else:
                self.stdout.write('❌ Not using Cloudinary storage for images!')
                
        except Exception as e:
            self.stdout.write(f'❌ Wagtail storage check failed: {e}')
        
        self.stdout.write('\n=== DEBUG COMPLETE ===')
