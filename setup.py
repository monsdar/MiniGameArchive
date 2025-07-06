#!/usr/bin/env python3
"""
Setup script for MiniGameArchive
Run this script to initialize the project with sample data
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/setup.log')
    ]
)

logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {description}: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def main():
    logger.info("Setting up MiniGameArchive...")
    logger.info("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        logger.error("manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    logger.info("Created data directory")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Running migrations"):
        sys.exit(1)
    
    # Load sample data
    if not run_command("python manage.py load_sample_data", "Loading sample data"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    logger.info("=" * 50)
    logger.info("Setup completed successfully!")
    logger.info("To start the development server: python manage.py runserver")
    logger.info("Admin panel: http://localhost:8000/admin/ (admin/admin123)")
    logger.info("Main site: http://localhost:8000/")

if __name__ == "__main__":
    main() 