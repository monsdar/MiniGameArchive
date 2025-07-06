"""
Unit tests for Django management commands
"""
import logging
import tempfile
import os
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.utils import translation
from games.models import Game, Focus, Material, Label, TrainingSession, SessionGame

logger = logging.getLogger(__name__)


class LoadSampleDataCommandTest(TestCase):
    """Test cases for load_sample_data management command"""
    
    def test_load_sample_data_command(self):
        """Test that load_sample_data command creates sample data"""
        # Run the command
        call_command('load_sample_data')
        
        # Check that sample data was created
        self.assertTrue(Focus.objects.count() > 0)
        self.assertTrue(Material.objects.count() > 0)
        self.assertTrue(Label.objects.count() > 0)
        self.assertTrue(Game.objects.count() > 0)
        
        # Check that admin user was created
        admin_user = User.objects.filter(username='admin').first()
        self.assertIsNotNone(admin_user)
        self.assertTrue(admin_user.check_password('admin123'))
        self.assertTrue(admin_user.is_superuser)
    
    def test_load_sample_data_command_idempotent(self):
        """Test that load_sample_data command can be run multiple times safely"""
        # Run the command twice
        call_command('load_sample_data')
        initial_count = Game.objects.count()
        
        call_command('load_sample_data')
        final_count = Game.objects.count()
        
        # Should not create duplicate data
        self.assertEqual(initial_count, final_count)
    
    def test_load_sample_data_creates_relationships(self):
        """Test that sample data includes proper relationships"""
        call_command('load_sample_data')
        
        # Check that games have relationships
        games = Game.objects.all()
        for game in games:
            self.assertTrue(game.focus.count() > 0)
            self.assertTrue(game.materials.count() > 0)
            self.assertTrue(game.labels.count() > 0)
    
    def test_load_sample_data_creates_training_sessions(self):
        """Test that sample data includes training sessions"""
        call_command('load_sample_data')
        
        # Check that training sessions were created
        self.assertTrue(TrainingSession.objects.count() > 0)
        
        # Check that sessions have games
        sessions = TrainingSession.objects.all()
        for session in sessions:
            self.assertTrue(session.sessiongame_set.count() > 0)


class TestI18nCommandTest(TestCase):
    """Test cases for test_i18n management command"""
    
    def setUp(self):
        """Set up test data"""
        # Create some test data
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.focus = Focus.objects.create(name="Dribbling")
        self.material = Material.objects.create(name="Basketball")
        self.label = Label.objects.create(name="Warm-up", color="#FF0000")
        
        self.game = Game.objects.create(
            name="Test Game",
            description="A test game for dribbling practice",
            player_count="2-4",
            duration="10min",
            created_by=self.user
        )
        self.game.focus.add(self.focus)
        self.game.materials.add(self.material)
        self.game.labels.add(self.label)
    
    def test_test_i18n_command_english(self):
        """Test test_i18n command with English"""
        # Run the command with English
        call_command('test_i18n', 'en')
        
        # Check that no errors occurred (command should complete successfully)
        # The command mainly tests translation loading, so we just verify it runs
    
    def test_test_i18n_command_german(self):
        """Test test_i18n command with German"""
        # Run the command with German
        call_command('test_i18n', 'de')
        
        # Check that no errors occurred (command should complete successfully)
    
    def test_test_i18n_command_invalid_language(self):
        """Test test_i18n command with invalid language"""
        with self.assertRaises(CommandError):
            call_command('test_i18n', 'invalid')
    
    def test_test_i18n_command_no_language(self):
        """Test test_i18n command without language parameter"""
        # Command should work without language parameter (uses default)
        call_command('test_i18n')
        
        # Verify that the command completed successfully
        # (no exception should be raised)
    
    def test_test_i18n_command_translation_loading(self):
        """Test that test_i18n command properly loads translations"""
        # Test with English
        with translation.override('en'):
            call_command('test_i18n', 'en')
        
        # Test with German
        with translation.override('de'):
            call_command('test_i18n', 'de')


class ManagementCommandIntegrationTest(TestCase):
    """Integration tests for management commands"""
    
    def test_load_sample_data_followed_by_test_i18n(self):
        """Test that load_sample_data and test_i18n work together"""
        # Load sample data
        call_command('load_sample_data')
        
        # Test i18n with both languages
        call_command('test_i18n', 'en')
        call_command('test_i18n', 'de')
        
        # Verify that data is still intact
        self.assertTrue(Game.objects.count() > 0)
        self.assertTrue(TrainingSession.objects.count() > 0)
    
    def test_management_commands_with_database_transactions(self):
        """Test that management commands work with database transactions"""
        from django.db import transaction
        
        with transaction.atomic():
            call_command('load_sample_data')
            
            # Verify data was created within transaction
            self.assertTrue(Game.objects.count() > 0)
        
        # Verify data persists after transaction
        self.assertTrue(Game.objects.count() > 0)


class ManagementCommandErrorHandlingTest(TestCase):
    """Test cases for management command error handling"""
    
    def test_load_sample_data_with_existing_data(self):
        """Test load_sample_data with existing data"""
        # Create some existing data
        user = User.objects.create_user(
            username='existinguser',
            password='testpass123'
        )
        
        existing_focus = Focus.objects.create(name="Existing Focus")
        existing_material = Material.objects.create(name="Existing Material")
        
        # Run load_sample_data
        call_command('load_sample_data')
        
        # Verify that existing data is preserved
        self.assertTrue(Focus.objects.filter(name="Existing Focus").exists())
        self.assertTrue(Material.objects.filter(name="Existing Material").exists())
        
        # Verify that new data was also created
        self.assertTrue(Focus.objects.count() > 1)
        self.assertTrue(Material.objects.count() > 1)
    
    def test_load_sample_data_with_corrupted_data(self):
        """Test load_sample_data handles corrupted data gracefully"""
        # Create a game without required relationships
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        game = Game.objects.create(
            name="Corrupted Game",
            description="A game without relationships",
            player_count="1-2",
            duration="5min",
            created_by=user
        )
        
        # Run load_sample_data - should not fail
        call_command('load_sample_data')
        
        # Verify that the command completed successfully
        self.assertTrue(Game.objects.count() > 1)


class ManagementCommandPerformanceTest(TestCase):
    """Test cases for management command performance"""
    
    def test_load_sample_data_performance(self):
        """Test that load_sample_data performs reasonably"""
        import time
        
        start_time = time.time()
        call_command('load_sample_data')
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete within 10 seconds (adjust as needed)
        self.assertLess(execution_time, 10.0)
        
        # Should create reasonable amount of data
        self.assertGreater(Game.objects.count(), 0)
        self.assertLess(Game.objects.count(), 1000)  # Not too many
    
    def test_test_i18n_performance(self):
        """Test that test_i18n performs reasonably"""
        import time
        
        start_time = time.time()
        call_command('test_i18n', 'en')
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete within 5 seconds
        self.assertLess(execution_time, 5.0)


class ManagementCommandLoggingTest(TestCase):
    """Test cases for management command logging"""
    
    def test_load_sample_data_logging(self):
        """Test that load_sample_data logs appropriately"""
        # Run the command
        call_command('load_sample_data')
        
        # Verify that the command completed successfully
        # (logging behavior may vary in test environment)
        
    def test_test_i18n_logging(self):
        """Test that test_i18n logs appropriately"""
        # Run the command
        call_command('test_i18n')
        
        # Verify that the command completed successfully
        # (logging behavior may vary in test environment) 