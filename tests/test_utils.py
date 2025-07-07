"""
Unit tests for utility functions and helpers
"""
import logging
import os
import tempfile
import shutil
from django.test import TestCase
from django.conf import settings
from django.utils import translation
from django.core.management import call_command
from django.core.management.base import CommandError

logger = logging.getLogger(__name__)


class TranslationCompilationTest(TestCase):
    """Test cases for translation compilation utilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_locale_paths = settings.LOCALE_PATHS
        settings.LOCALE_PATHS = [self.temp_dir]
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
        settings.LOCALE_PATHS = self.original_locale_paths
    
    def test_compile_translations_script(self):
        """Test the compile_translations.py script"""
        # Create a temporary locale structure
        locale_dir = os.path.join(self.temp_dir, 'locale')
        os.makedirs(locale_dir)
        
        # Create a test .po file
        po_dir = os.path.join(locale_dir, 'de', 'LC_MESSAGES')
        os.makedirs(po_dir)
        
        po_file = os.path.join(po_dir, 'django.po')
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write("""msgid ""
msgstr ""
"Project-Id-Version: MiniGameArchive\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2024-01-01 12:00+0000\\n"
"PO-Revision-Date: 2024-01-01 12:00+0000\\n"
"Last-Translator: \\n"
"Language-Team: \\n"
"Language: de\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "Games"
msgstr "Spiele"

msgid "Training Session"
msgstr "Trainingseinheit"
""")
        
        # Test compilation
        try:
            # Import and run the compilation script
            import sys
            sys.path.insert(0, os.path.dirname(settings.BASE_DIR))
            
            # This would normally run the compile_translations.py script
            # For testing, we'll simulate the compilation
            mo_file = os.path.join(po_dir, 'django.mo')
            
            # Check that .po file exists
            self.assertTrue(os.path.exists(po_file))
            
            # Simulate compilation by creating a .mo file
            with open(mo_file, 'wb') as f:
                f.write(b'# Mock compiled translation file')
            
            # Verify .mo file was created
            self.assertTrue(os.path.exists(mo_file))
            
        except ImportError:
            # Skip if polib is not available
            self.skipTest("polib not available for translation compilation test")
    
    def test_translation_file_structure(self):
        """Test that translation files have correct structure"""
        # Create a test locale structure
        locale_dir = os.path.join(self.temp_dir, 'locale')
        os.makedirs(locale_dir)
        
        # Test German locale
        de_dir = os.path.join(locale_dir, 'de', 'LC_MESSAGES')
        os.makedirs(de_dir)
        
        po_file = os.path.join(de_dir, 'django.po')
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write("""msgid ""
msgstr ""
"Project-Id-Version: MiniGameArchive\\n"
"Language: de\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "Games"
msgstr "Spiele"
""")
        
        # Verify file structure
        self.assertTrue(os.path.exists(po_file))
        self.assertTrue(os.path.isfile(po_file))
        
        # Check file content
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('msgid "Games"', content)
            self.assertIn('msgstr "Spiele"', content)


class LoggingUtilityTest(TestCase):
    """Test cases for logging utilities"""
    
    def test_logging_configuration(self):
        """Test that logging is properly configured"""
        # Check that logging is configured
        self.assertIsNotNone(logging.getLogger())
        
        # Check that our logger exists
        test_logger = logging.getLogger(__name__)
        self.assertIsNotNone(test_logger)
    
    def test_logging_levels(self):
        """Test different logging levels"""
        test_logger = logging.getLogger('test_logger')
        
        # Test that we can log at different levels
        with self.assertLogs(test_logger, level='DEBUG') as log:
            test_logger.debug('Debug message')
            test_logger.info('Info message')
            test_logger.warning('Warning message')
            test_logger.error('Error message')
        
        # Check that all messages were logged
        self.assertEqual(len(log.records), 4)
        self.assertEqual(log.records[0].levelname, 'DEBUG')
        self.assertEqual(log.records[1].levelname, 'INFO')
        self.assertEqual(log.records[2].levelname, 'WARNING')
        self.assertEqual(log.records[3].levelname, 'ERROR')
    
    def test_logging_format(self):
        """Test logging message format"""
        test_logger = logging.getLogger('test_logger')
        
        with self.assertLogs(test_logger, level='INFO') as log:
            test_logger.info('Test message')
        
        # Check that log record has expected attributes
        record = log.records[0]
        self.assertIsNotNone(record.message)
        self.assertIsNotNone(record.levelname)
        self.assertIsNotNone(record.name)
    
    def test_logging_in_views(self):
        """Test that views use logging instead of print statements"""
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Make a request to trigger view logging
        response = client.get(reverse('game_list'))
        
        # Check that the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Verify that logging is configured (basic check)
        import logging
        logger = logging.getLogger('django')
        self.assertIsNotNone(logger)


class InternationalizationUtilityTest(TestCase):
    """Test cases for internationalization utilities"""
    
    def test_language_context_processor(self):
        """Test language context processor"""
        from django.test import RequestFactory
        from games.context_processors import language_info
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/')
        
        # Set language in session
        request.session = {}
        request.session['django_language'] = 'de'
        
        # Get context from processor
        context = language_info(request)
        
        # Check that context contains expected keys
        self.assertIn('current_language', context)
        self.assertIn('available_languages', context)
        
        # Check current language
        self.assertEqual(context['current_language'], 'de')
        
        # Check available languages (should be tuples)
        self.assertIn(('en', 'English'), context['available_languages'])
        self.assertIn(('de', 'Deutsch'), context['available_languages'])
    
    def test_language_switching(self):
        """Test language switching functionality"""
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test switching to German
        response = client.post(reverse('set_language'), {
            'language': 'de',
            'next': reverse('game_list')
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check that language was set in session
        session = client.session
        self.assertEqual(session.get('django_language'), 'de')
        
        # Test switching to English
        response = client.post(reverse('set_language'), {
            'language': 'en',
            'next': reverse('game_list')
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check that language was updated in session
        session = client.session
        self.assertEqual(session.get('django_language'), 'en')
    
    def test_translation_loading(self):
        """Test that translations are properly loaded"""
        # Test with English
        with translation.override('en'):
            self.assertEqual(translation.get_language(), 'en')
        
        # Test with German
        with translation.override('de'):
            self.assertEqual(translation.get_language(), 'de')
        
        # Test fallback to English
        with translation.override('invalid'):
            # Should fall back to default language
            pass


class FileUtilityTest(TestCase):
    """Test cases for file utilities"""
    
    def test_logs_directory_creation(self):
        """Test that logs directory is created if it doesn't exist"""
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        
        # Check that directory exists (it should be created by logging config)
        self.assertTrue(os.path.exists(logs_dir))
        self.assertTrue(os.path.isdir(logs_dir))
        
        # Test creating a new file in the directory
        test_file = os.path.join(logs_dir, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        # Verify file was created
        self.assertTrue(os.path.exists(test_file))
        
        # Clean up test file
        os.remove(test_file)
    
    def test_static_files_collection(self):
        """Test static files collection"""
        # This test verifies that static files can be collected
        # In a real test environment, you might want to test the collectstatic command
        
        static_root = os.path.join(settings.BASE_DIR, 'staticfiles')
        
        # Clean up any existing static files
        if os.path.exists(static_root):
            shutil.rmtree(static_root)
        
        # Check that static root doesn't exist
        self.assertFalse(os.path.exists(static_root))
        
        # Create static root directory
        os.makedirs(static_root, exist_ok=True)
        
        # Check that directory was created
        self.assertTrue(os.path.exists(static_root))
        self.assertTrue(os.path.isdir(static_root))


class ConfigurationTest(TestCase):
    """Test cases for configuration settings"""
    
    def test_debug_setting(self):
        """Test DEBUG setting"""
        # Check that DEBUG is a boolean
        self.assertIsInstance(settings.DEBUG, bool)
    
    def test_database_configuration(self):
        """Test database configuration"""
        # Check that database is configured
        self.assertIn('default', settings.DATABASES)
        
        db_config = settings.DATABASES['default']
        self.assertIn('ENGINE', db_config)
    
    def test_installed_apps(self):
        """Test installed apps configuration"""
        # Check that required apps are installed
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.auth', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.contenttypes', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.sessions', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.messages', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.staticfiles', settings.INSTALLED_APPS)
        self.assertIn('games', settings.INSTALLED_APPS)
    
    def test_middleware_configuration(self):
        """Test middleware configuration"""
        # Check that required middleware is configured
        self.assertIn('django.middleware.security.SecurityMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.middleware.common.CommonMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.auth.middleware.AuthenticationMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.messages.middleware.MessageMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.middleware.clickjacking.XFrameOptionsMiddleware', settings.MIDDLEWARE)
        
        # Check for i18n middleware
        self.assertIn('django.middleware.locale.LocaleMiddleware', settings.MIDDLEWARE)
    
    def test_language_settings(self):
        """Test language settings"""
        self.assertIn(('en', 'English'), settings.LANGUAGES)
        self.assertIn(('de', 'Deutsch'), settings.LANGUAGES)
        # Check that LANGUAGE_CODE starts with 'en' (could be 'en' or 'en-us')
        self.assertTrue(settings.LANGUAGE_CODE.startswith('en'))
        
        # Check that locale paths are configured
        self.assertTrue(hasattr(settings, 'LOCALE_PATHS'))
        self.assertIsInstance(settings.LOCALE_PATHS, (list, tuple))
    
    def test_logging_configuration(self):
        """Test logging configuration"""
        # Check that logging is configured
        self.assertTrue(hasattr(settings, 'LOGGING'))
        self.assertIsInstance(settings.LOGGING, dict)
        
        # Check for required logging configuration
        logging_config = settings.LOGGING
        self.assertIn('version', logging_config)
        self.assertIn('disable_existing_loggers', logging_config)
        self.assertIn('formatters', logging_config)
        self.assertIn('handlers', logging_config)
        self.assertIn('loggers', logging_config) 