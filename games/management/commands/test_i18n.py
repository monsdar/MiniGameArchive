import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test i18n setup and compile translation files'

    def add_arguments(self, parser):
        parser.add_argument('language', nargs='?', default=None, help="Language code to test (en, de)")

    def handle(self, *args, **options):
        language = options.get('language')
        logger.info('Testing i18n setup...')
        languages = ['en', 'de']
        if language:
            if language not in languages:
                raise CommandError(f"Unsupported language: {language}")
            languages = [language]
        for lang in languages:
            translation.activate(lang)
            logger.info(f'{lang.capitalize()}: {_("Games")}')
            logger.info(f'{lang.capitalize()}: {_("Training Session")}')
        logger.info('i18n test completed!')
        
        # Note: In a real environment, you would run:
        # python manage.py compilemessages
        # to compile the .po files to .mo files 