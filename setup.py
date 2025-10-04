#!/usr/bin/env python3
"""
Setup script for MarketingNyt.dk
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None


def check_requirements():
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ is required")
        return False
    
    # Check Poetry
    if not shutil.which("poetry"):
        print("❌ Poetry is not installed. Please install it first:")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
        return False
    
    print("✅ All requirements met")
    return True


def setup_environment():
    """Setup the development environment."""
    print("\n🚀 Setting up MarketingNyt.dk development environment\n")
    
    if not check_requirements():
        return False
    
    # Install dependencies
    if not run_command("poetry install", "Installing Python dependencies"):
        return False
    
    # Copy environment file
    if not Path(".env").exists():
        if Path(".env.example").exists():
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from .env.example")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("ℹ️  .env file already exists")
    
    # Run migrations
    if not run_command("poetry run python manage.py migrate", "Running database migrations"):
        return False
    
    # Collect static files
    if not run_command("poetry run python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Create sample data
    create_sample = input("\n📝 Create sample data? (y/N): ").lower().strip()
    if create_sample in ['y', 'yes']:
        if run_command("poetry run python manage.py create_sample_data", "Creating sample data"):
            print("✅ Sample data created")
        else:
            print("⚠️  Sample data creation failed, but setup can continue")
    
    # Create superuser
    create_superuser = input("\n👤 Create superuser account? (y/N): ").lower().strip()
    if create_superuser in ['y', 'yes']:
        print("Creating superuser account...")
        os.system("poetry run python manage.py createsuperuser")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your settings")
    print("2. Run 'make run' or 'poetry run python manage.py runserver'")
    print("3. Visit http://localhost:8000 to see your site")
    print("4. Visit http://localhost:8000/admin/ for Wagtail admin")
    
    return True


if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
