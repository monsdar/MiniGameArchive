"""
Unit tests for Django models
"""
import logging
import time
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from games.models import Game, Focus, Material, Label, TrainingSession, SessionGame
from django.db import models

logger = logging.getLogger(__name__)


class FocusModelTest(TestCase):
    """Test cases for Focus model"""
    
    def setUp(self):
        """Set up test data"""
        self.focus = Focus.objects.create(name="Dribbling")
    
    def test_focus_creation(self):
        """Test that a focus can be created"""
        self.assertEqual(self.focus.name, "Dribbling")
        self.assertEqual(str(self.focus), "Dribbling")
    
    def test_focus_unique_name(self):
        """Test that focus names must be unique"""
        with self.assertRaises(Exception):
            Focus.objects.create(name="Dribbling")
    
    def test_focus_ordering(self):
        """Test that focuses are ordered by name"""
        Focus.objects.create(name="Shooting")
        Focus.objects.create(name="Passing")
        
        focuses = Focus.objects.all()
        self.assertEqual(focuses[0].name, "Dribbling")
        self.assertEqual(focuses[1].name, "Passing")
        self.assertEqual(focuses[2].name, "Shooting")


class MaterialModelTest(TestCase):
    """Test cases for Material model"""
    
    def setUp(self):
        """Set up test data"""
        self.material = Material.objects.create(name="Basketball")
    
    def test_material_creation(self):
        """Test that a material can be created"""
        self.assertEqual(self.material.name, "Basketball")
        self.assertEqual(str(self.material), "Basketball")
    
    def test_material_unique_name(self):
        """Test that material names must be unique"""
        with self.assertRaises(Exception):
            Material.objects.create(name="Basketball")


class LabelModelTest(TestCase):
    """Test cases for Label model"""
    
    def setUp(self):
        """Set up test data"""
        self.label = Label.objects.create(
            name="Warm-up",
            color="#FF0000"
        )
    
    def test_label_creation(self):
        """Test that a label can be created"""
        self.assertEqual(self.label.name, "Warm-up")
        self.assertEqual(self.label.color, "#FF0000")
        self.assertEqual(str(self.label), "Warm-up")
    
    def test_label_unique_name(self):
        """Test that label names must be unique"""
        with self.assertRaises(Exception):
            Label.objects.create(name="Warm-up", color="#00FF00")


class GameModelTest(TestCase):
    """Test cases for Game model"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_game_creation(self):
        """Test that a game can be created"""
        self.assertEqual(self.game.name, "Test Game")
        self.assertEqual(self.game.description, "A test game for dribbling practice")
        self.assertEqual(self.game.player_count, "2-4")
        self.assertEqual(self.game.duration, "10min")
        self.assertEqual(self.game.created_by, self.user)
        self.assertEqual(str(self.game), "Test Game")
    
    def test_game_get_player_count_display(self):
        """Test player count display method"""
        self.assertEqual(self.game.get_player_count_display(), "2-4")
    
    def test_game_get_duration_display(self):
        """Test duration display method"""
        self.assertEqual(self.game.get_duration_display(), "10 minutes")
    
    def test_game_get_materials_display(self):
        """Test materials display method"""
        self.assertEqual(self.game.get_materials_display(), "Basketball")
    
    def test_game_focus_relationship(self):
        """Test focus relationship"""
        self.assertIn(self.focus, self.game.focus.all())
        self.assertEqual(self.game.focus.count(), 1)
    
    def test_game_materials_relationship(self):
        """Test materials relationship"""
        self.assertIn(self.material, self.game.materials.all())
        self.assertEqual(self.game.materials.count(), 1)
    
    def test_game_labels_relationship(self):
        """Test labels relationship"""
        self.assertIn(self.label, self.game.labels.all())
        self.assertEqual(self.game.labels.count(), 1)
    
    def test_game_search(self):
        """Test game search functionality"""
        # Create another game for search testing
        Game.objects.create(
            name="Shooting Practice",
            description="Practice shooting from different positions",
            player_count="1-2",
            duration="15min",
            created_by=self.user
        )
        
        # Test search by name
        results = Game.objects.filter(name__icontains="Test")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.game)
        
        # Test search by description
        results = Game.objects.filter(description__icontains="dribbling")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.game)


class TrainingSessionModelTest(TestCase):
    """Test cases for TrainingSession model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.session = TrainingSession.objects.create(
            name="Test Session",
            description="A test training session",
            created_by=self.user
        )
    
    def test_session_creation(self):
        """Test that a training session can be created"""
        self.assertEqual(self.session.name, "Test Session")
        self.assertEqual(self.session.description, "A test training session")
        self.assertEqual(self.session.created_by, self.user)
        self.assertEqual(str(self.session), "Test Session")
    
    def test_session_ordering(self):
        """Test that sessions are ordered by creation date"""
        # Create another session with a small delay to ensure different timestamps
        time.sleep(0.001)  # 1ms delay
        second_session = TrainingSession.objects.create(
            name="Second Session",
            description="Another test session",
            created_by=self.user
        )
        
        # Get all sessions ordered by creation date (newest first)
        sessions = list(TrainingSession.objects.order_by('-created_at'))
        self.assertEqual(len(sessions), 2)
        
        # Verify that the second session (created later) comes first
        self.assertEqual(sessions[0], second_session)  # Newest first
        self.assertEqual(sessions[1], self.session)
        
        # Also verify the timestamps
        self.assertGreater(second_session.created_at, self.session.created_at)


class SessionGameModelTest(TestCase):
    """Test cases for SessionGame model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.game = Game.objects.create(
            name="Test Game",
            description="A test game",
            player_count="2-4",
            duration="10min",
            created_by=self.user
        )
        
        self.session = TrainingSession.objects.create(
            name="Test Session",
            description="A test training session",
            created_by=self.user
        )
        
        self.session_game = SessionGame.objects.create(
            session=self.session,
            game=self.game,
            order=1
        )
    
    def test_session_game_creation(self):
        """Test that a session game can be created"""
        self.assertEqual(str(self.session_game), "Test Session - Test Game (Order: 1)")
    
    def test_session_game_ordering(self):
        """Test that session games are ordered by order field"""
        game2 = Game.objects.create(
            name="Second Game",
            description="Another test game",
            player_count="1-2",
            duration="5min",
            created_by=self.user
        )
        
        session_game2 = SessionGame.objects.create(
            session=self.session,
            game=game2,
            order=2
        )
        
        session_games = SessionGame.objects.filter(session=self.session)
        self.assertEqual(session_games[0], self.session_game)
        self.assertEqual(session_games[1], session_game2)
    
    def test_session_game_unique_constraint(self):
        """Test that a game can only be added once to a session with the same order"""
        with self.assertRaises(Exception):
            SessionGame.objects.create(
                session=self.session,
                game=self.game,
                order=1  # Same order as the existing session game
            )


class ModelIntegrationTest(TestCase):
    """Integration tests for model relationships"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create focuses
        self.dribbling = Focus.objects.create(name="Dribbling")
        self.shooting = Focus.objects.create(name="Shooting")
        
        # Create materials
        self.basketball = Material.objects.create(name="Basketball")
        self.hoop = Material.objects.create(name="Hoop")
        
        # Create labels
        self.warmup = Label.objects.create(name="Warm-up", color="#FF0000")
        self.advanced = Label.objects.create(name="Advanced", color="#00FF00")
        
        # Create games
        self.game1 = Game.objects.create(
            name="Dribbling Practice",
            description="Practice dribbling skills",
            player_count="1-2",
            duration="10min",
            created_by=self.user
        )
        self.game1.focus.add(self.dribbling)
        self.game1.materials.add(self.basketball)
        self.game1.labels.add(self.warmup)
        
        self.game2 = Game.objects.create(
            name="Shooting Practice",
            description="Practice shooting from different positions",
            player_count="2-4",
            duration="15min",
            created_by=self.user
        )
        self.game2.focus.add(self.shooting)
        self.game2.materials.add(self.basketball, self.hoop)
        self.game2.labels.add(self.advanced)
        
        # Create training session
        self.session = TrainingSession.objects.create(
            name="Complete Training",
            description="A complete training session",
            created_by=self.user
        )
        
        # Add games to session
        SessionGame.objects.create(
            session=self.session,
            game=self.game1,
            order=1
        )
        SessionGame.objects.create(
            session=self.session,
            game=self.game2,
            order=2
        )
    
    def test_game_focus_filtering(self):
        """Test filtering games by focus"""
        dribbling_games = Game.objects.filter(focus=self.dribbling)
        self.assertEqual(dribbling_games.count(), 1)
        self.assertEqual(dribbling_games.first(), self.game1)
        
        shooting_games = Game.objects.filter(focus=self.shooting)
        self.assertEqual(shooting_games.count(), 1)
        self.assertEqual(shooting_games.first(), self.game2)
    
    def test_game_materials_filtering(self):
        """Test filtering games by materials"""
        basketball_games = Game.objects.filter(materials=self.basketball)
        self.assertEqual(basketball_games.count(), 2)
        
        hoop_games = Game.objects.filter(materials=self.hoop)
        self.assertEqual(hoop_games.count(), 1)
        self.assertEqual(hoop_games.first(), self.game2)
    
    def test_game_labels_filtering(self):
        """Test filtering games by labels"""
        warmup_games = Game.objects.filter(labels=self.warmup)
        self.assertEqual(warmup_games.count(), 1)
        self.assertEqual(warmup_games.first(), self.game1)
        
        advanced_games = Game.objects.filter(labels=self.advanced)
        self.assertEqual(advanced_games.count(), 1)
        self.assertEqual(advanced_games.first(), self.game2)
    
    def test_session_games_relationship(self):
        """Test session games relationship"""
        session_games = self.session.sessiongame_set.all().order_by('order')
        self.assertEqual(session_games.count(), 2)
        self.assertEqual(session_games[0].game, self.game1)
        self.assertEqual(session_games[1].game, self.game2)
    
    def test_user_games_relationship(self):
        """Test user games relationship"""
        user_games = Game.objects.filter(created_by=self.user)
        self.assertEqual(user_games.count(), 2)
    
    def test_user_sessions_relationship(self):
        """Test user sessions relationship"""
        user_sessions = TrainingSession.objects.filter(created_by=self.user)
        self.assertEqual(user_sessions.count(), 1)
        self.assertEqual(user_sessions.first(), self.session) 