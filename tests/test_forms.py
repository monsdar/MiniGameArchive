"""
Unit tests for Django forms
"""
import logging
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from games.forms import GameForm, TrainingSessionForm, GameSuggestionForm
from games.models import Game, Focus, Material, Label, TrainingSession

logger = logging.getLogger(__name__)


class GameFormTest(TestCase):
    """Test cases for GameForm"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.focus = Focus.objects.create(name="Dribbling")
        self.material = Material.objects.create(name="Basketball")
        self.label = Label.objects.create(name="Warm-up", color="#FF0000")
        
        # Create a test game for update tests
        self.game = Game.objects.create(
            name='Test Game',
            description='A test game for dribbling practice',
            player_count='1-2',
            duration='10min',
            variants='Some variants',
            created_by=self.user
        )
        self.game.focus.add(self.focus)
        self.game.materials.add(self.material)
        self.game.labels.add(self.label)
    
    def test_game_form_valid(self):
        """Test that GameForm is valid with correct data"""
        form_data = {
            'name': 'Test Game',
            'description': 'A test game for dribbling practice',
            'player_count': '1-2',
            'duration': '10min',
            'variants': 'Some variants',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
        }
        
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_game_form_invalid_missing_required(self):
        """Test that GameForm is invalid without required fields"""
        form_data = {
            'description': 'A test game for dribbling practice',
            'player_count': '1-2',
            'duration': '10min',
        }
        
        form = GameForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_game_form_save(self):
        """Test that GameForm saves correctly"""
        form_data = {
            'name': 'Test Game',
            'description': 'A test game for dribbling practice',
            'player_count': '1-2',
            'duration': '10min',
            'variants': 'Some variants',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
        }
        
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        game = form.save(commit=False)
        game.created_by = self.user
        game.save()
        form.save_m2m()  # Save many-to-many relationships
        
        self.assertEqual(game.name, 'Test Game')
        self.assertEqual(game.description, 'A test game for dribbling practice')
        self.assertEqual(game.player_count, '1-2')
        self.assertEqual(game.duration, '10min')
        self.assertEqual(game.variants, 'Some variants')
        self.assertEqual(game.created_by, self.user)
        
        # Check many-to-many relationships
        self.assertIn(self.focus, game.focus.all())
        self.assertIn(self.material, game.materials.all())
        self.assertIn(self.label, game.labels.all())
    
    def test_game_form_update(self):
        """Test that GameForm updates existing game correctly"""
        form_data = {
            'name': 'Updated Game',
            'description': 'Updated description',
            'player_count': '5-6',  # valid choice
            'duration': '15min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
            'variants': 'Updated variants'
        }
        
        form = GameForm(data=form_data, instance=self.game)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())
        
        updated_game = form.save(commit=False)
        updated_game.save()
        form.save_m2m()  # Save many-to-many relationships
        
        self.assertEqual(updated_game.name, 'Updated Game')
        self.assertEqual(updated_game.description, 'Updated description')
        self.assertEqual(updated_game.player_count, '5-6')
        self.assertEqual(updated_game.duration, '15min')
        self.assertIn(self.focus, updated_game.focus.all())
        self.assertIn(self.material, updated_game.materials.all())
        self.assertIn(self.label, updated_game.labels.all())


class TrainingSessionFormTest(TestCase):
    """Test cases for TrainingSessionForm"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_training_session_form_valid(self):
        """Test that TrainingSessionForm is valid with correct data"""
        form_data = {
            'name': 'Test Training Session',
            'description': 'A test training session',
        }
        
        form = TrainingSessionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_training_session_form_invalid_missing_required(self):
        """Test that TrainingSessionForm is invalid without required fields"""
        form_data = {
            'description': 'A test training session',
        }
        
        form = TrainingSessionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_training_session_form_save(self):
        """Test that TrainingSessionForm saves correctly"""
        form_data = {
            'name': 'Test Training Session',
            'description': 'A test training session',
        }
        
        form = TrainingSessionForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        session = form.save(commit=False)
        session.created_by = self.user
        session.save()
        
        self.assertEqual(session.name, 'Test Training Session')
        self.assertEqual(session.description, 'A test training session')
        self.assertEqual(session.created_by, self.user)
    
    def test_training_session_form_update(self):
        """Test that TrainingSessionForm updates existing session correctly"""
        # Create initial session
        session = TrainingSession.objects.create(
            name='Initial Session',
            description='Initial description',
            created_by=self.user
        )
        
        # Update with form
        form_data = {
            'name': 'Updated Session',
            'description': 'Updated description',
        }
        
        form = TrainingSessionForm(data=form_data, instance=session)
        self.assertTrue(form.is_valid())
        
        updated_session = form.save()
        
        self.assertEqual(updated_session.name, 'Updated Session')
        self.assertEqual(updated_session.description, 'Updated description')


class GameSuggestionFormTest(TestCase):
    """Test cases for GameSuggestionForm"""
    
    def setUp(self):
        """Set up test data"""
        self.focus = Focus.objects.create(name="Dribbling")
        self.material = Material.objects.create(name="Basketball")
        self.label = Label.objects.create(name="Warm-up", color="#FF0000")
    
    def test_game_suggestion_form_valid(self):
        """Test that GameSuggestionForm is valid with correct data"""
        form_data = {
            'name': 'Suggested Game',
            'description': 'A suggested game',
            'player_count': '1-2',
            'duration': '10min',
            'variants': 'Some variants',
            'email': 'test@example.com',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
        }
        
        form = GameSuggestionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_game_suggestion_form_invalid_missing_required(self):
        """Test that GameSuggestionForm is invalid without required fields"""
        form_data = {
            'description': 'A suggested game',
            'player_count': '1-2',
            'duration': '10min',
            'email': 'test@example.com',
        }
        
        form = GameSuggestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_game_suggestion_form_invalid_data(self):
        """Test that GameSuggestionForm handles invalid data correctly"""
        form_data = {
            'name': '',  # Required field missing
            'description': 'A test game',
            'player_count': 'invalid',  # Invalid choice
            'duration': '10min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id]
        }
        
        form = GameSuggestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('player_count', form.errors)
    
    def test_game_suggestion_form_valid_without_optional_fields(self):
        """Test that GameSuggestionForm is valid without optional fields"""
        form_data = {
            'name': 'Test Game',
            'description': 'A test game',
            'player_count': '3-4',
            'duration': '10min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id]
        }
        
        form = GameSuggestionForm(data=form_data)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())
    
    def test_game_suggestion_form_clean_methods(self):
        """Test custom clean methods in GameSuggestionForm"""
        form_data = {
            'name': 'Test Game',
            'description': 'A test game',
            'player_count': '3-4',
            'duration': '10min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
            'variants': 'Some variants'
        }
        
        form = GameSuggestionForm(data=form_data)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        
        # Test that cleaned data contains expected fields
        self.assertEqual(cleaned_data['name'], 'Test Game')
        self.assertEqual(cleaned_data['description'], 'A test game')
        self.assertEqual(cleaned_data['player_count'], '3-4')
        self.assertEqual(cleaned_data['duration'], '10min')


class FormIntegrationTest(TestCase):
    """Integration tests for forms with models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.focus = Focus.objects.create(name="Dribbling")
        self.material = Material.objects.create(name="Basketball")
        self.label = Label.objects.create(name="Warm-up", color="#FF0000")
    
    def test_game_form_with_existing_relationships(self):
        """Test GameForm with existing focus, materials, and labels"""
        form_data = {
            'name': 'Integration Test Game',
            'description': 'A game for integration testing',
            'player_count': '1-2',
            'duration': '10min',
            'variants': 'Integration variants',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
        }
        
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        game = form.save(commit=False)
        game.created_by = self.user
        game.save()
        form.save_m2m()
        
        # Verify the game was created with all relationships
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.first()
        self.assertEqual(game.focus.count(), 1)
        self.assertEqual(game.materials.count(), 1)
        self.assertEqual(game.labels.count(), 1)
    
    def test_training_session_form_creates_session(self):
        """Test that TrainingSessionForm creates a session correctly"""
        form_data = {
            'name': 'Integration Test Session',
            'description': 'A session for integration testing',
        }
        
        form = TrainingSessionForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        session = form.save(commit=False)
        session.created_by = self.user
        session.save()
        
        # Verify the session was created
        self.assertEqual(TrainingSession.objects.count(), 1)
        session = TrainingSession.objects.first()
        self.assertEqual(session.name, 'Integration Test Session')
        self.assertEqual(session.created_by, self.user)
    
    def test_form_validation_error_handling(self):
        """Test that forms properly handle validation errors"""
        # Test GameForm with missing required fields
        form_data = {
            'name': '',  # Required field missing
            'description': 'A test game',
            'player_count': '2-4',
            'duration': '10min'
        }
        
        form = GameForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('focus', form.errors)  # focus is required
        
        # Test TrainingSessionForm with invalid data
        form_data = {
            'name': '',  # Empty name should cause validation error
            'description': 'A test session',
        }
        
        form = TrainingSessionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test GameSuggestionForm with missing required fields
        form_data = {
            'name': '',  # Required field missing
            'description': 'A suggested game',
            'player_count': '1-2',
            'duration': '10min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
        }
        
        form = GameSuggestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors) 