"""
Management command to test Cloudinary connection.
"""

import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test Cloudinary connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write('Testing Cloudinary connection...')
        
        # Check environment variables
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        self.stdout.write(f'CLOUDINARY_CLOUD_NAME: {cloud_name}')
        self.stdout.write(f'CLOUDINARY_API_KEY: {api_key}')
        self.stdout.write(f'CLOUDINARY_API_SECRET: {"*" * len(api_secret) if api_secret else None}')
        
        if not all([cloud_name, api_key, api_secret]):
            self.stdout.write(self.style.ERROR('Missing Cloudinary environment variables!'))
            return
        
        # Test Cloudinary import and configuration
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            self.stdout.write('Cloudinary modules imported successfully')
            
            # Test API connection
            try:
                result = cloudinary.api.ping()
                self.stdout.write(self.style.SUCCESS(f'Cloudinary API ping successful: {result}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Cloudinary API ping failed: {e}'))
            
            # Test upload with a simple text file
            try:
                result = cloudinary.uploader.upload(
                    "data:text/plain;base64,SGVsbG8gV29ybGQ=",  # "Hello World" in base64
                    public_id="test_connection",
                    resource_type="raw"
                )
                self.stdout.write(self.style.SUCCESS(f'Test upload successful: {result["secure_url"]}'))
                
                # Clean up test file
                cloudinary.uploader.destroy("test_connection", resource_type="raw")
                self.stdout.write('Test file cleaned up')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Test upload failed: {e}'))
                
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'Failed to import Cloudinary: {e}'))
        
        # Check Django storage configuration
        from django.conf import settings
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {getattr(settings, "DEFAULT_FILE_STORAGE", "Not set")}')
        self.stdout.write(f'WAGTAILIMAGES_IMAGE_FILE_STORAGE: {getattr(settings, "WAGTAILIMAGES_IMAGE_FILE_STORAGE", "Not set")}')
        self.stdout.write(f'WAGTAILDOCS_DOCUMENT_FILE_STORAGE: {getattr(settings, "WAGTAILDOCS_DOCUMENT_FILE_STORAGE", "Not set")}')
        
        self.stdout.write('Cloudinary test complete!')
