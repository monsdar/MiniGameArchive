#!/usr/bin/env python
"""
Script to compile Django translation files from .po to .mo format using polib.
"""

import polib
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/compile_translations.log')
    ]
)

logger = logging.getLogger(__name__)

def compile_po_to_mo(po_file_path, mo_file_path):
    """Compile a .po file to .mo format using polib"""
    logger.info(f"Compiling {po_file_path} to {mo_file_path}")
    
    try:
        # Load the .po file
        po = polib.pofile(str(po_file_path))
        
        # Save as .mo file
        po.save_as_mofile(str(mo_file_path))
        
        translated_count = len([entry for entry in po if entry.msgstr])
        logger.info(f"Successfully created {mo_file_path}")
        logger.info(f"  - {len(po)} messages processed")
        logger.info(f"  - {translated_count} messages translated")
        
    except Exception as e:
        logger.error(f"Error compiling {po_file_path}: {e}")

def main():
    """Compile all .po files in the locale directory"""
    locale_dir = Path('locale')
    
    if not locale_dir.exists():
        logger.error("Locale directory not found!")
        return
    
    compiled_count = 0
    
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir() and lang_dir.name in ['de', 'en']:
            lc_messages_dir = lang_dir / 'LC_MESSAGES'
            if lc_messages_dir.exists():
                po_file = lc_messages_dir / 'django.po'
                mo_file = lc_messages_dir / 'django.mo'
                
                if po_file.exists():
                    compile_po_to_mo(po_file, mo_file)
                    compiled_count += 1
                else:
                    logger.warning(f"No .po file found in {lc_messages_dir}")
    
    if compiled_count > 0:
        logger.info(f"Successfully compiled {compiled_count} translation file(s)")
        logger.info("You can now test the language switching!")
    else:
        logger.warning("No translation files were compiled")

if __name__ == '__main__':
    main() 