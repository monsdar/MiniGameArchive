from django.test import TestCase
from django.contrib.auth.models import User
from games.models import Language, Game, Focus, Material, Label


class LanguageFieldTest(TestCase):
    """Test the new multi-selection language field functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create languages
        self.english, _ = Language.objects.get_or_create(code='en', defaults={'name': 'English'})
        self.german, _ = Language.objects.get_or_create(code='de', defaults={'name': 'Deutsch'})
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create focus areas
        self.focus = Focus.objects.create(name='Dribbling', description='Ball handling skills')
        self.focus.languages.add(self.english, self.german)
        
        # Create materials
        self.material = Material.objects.create(name='Basketball', description='Standard basketball')
        self.material.languages.add(self.english, self.german)
        
        # Create labels
        self.label = Label.objects.create(name='Beginner', color='#28a745')
        self.label.languages.add(self.english)
        
        # Create a game
        self.game = Game.objects.create(
            name='Basic Dribbling',
            description='Simple dribbling exercise',
            player_count='1-2',
            duration='10min',
            created_by=self.user
        )
        self.game.focus.add(self.focus)
        self.game.materials.add(self.material)
        self.game.labels.add(self.label)
        self.game.languages.add(self.english, self.german)
    
    def test_language_model(self):
        """Test Language model creation and string representation"""
        self.assertEqual(str(self.english), 'English')
        self.assertEqual(str(self.german), 'Deutsch')
        self.assertEqual(self.english.code, 'en')
        self.assertEqual(self.german.code, 'de')
    
    def test_focus_languages(self):
        """Test that focus areas can have multiple languages"""
        self.assertEqual(self.focus.languages.count(), 2)
        self.assertIn(self.english, self.focus.languages.all())
        self.assertIn(self.german, self.focus.languages.all())
    
    def test_material_languages(self):
        """Test that materials can have multiple languages"""
        self.assertEqual(self.material.languages.count(), 2)
        self.assertIn(self.english, self.material.languages.all())
        self.assertIn(self.german, self.material.languages.all())
    
    def test_label_languages(self):
        """Test that labels can have multiple languages"""
        self.assertEqual(self.label.languages.count(), 1)
        self.assertIn(self.english, self.label.languages.all())
        self.assertNotIn(self.german, self.label.languages.all())
    
    def test_game_languages(self):
        """Test that games can have multiple languages"""
        self.assertEqual(self.game.languages.count(), 2)
        self.assertIn(self.english, self.game.languages.all())
        self.assertIn(self.german, self.game.languages.all())
    
    def test_get_languages_display(self):
        """Test the get_languages_display method"""
        display = self.game.get_languages_display()
        self.assertIn(display, ['English, Deutsch', 'Deutsch, English'])
        self.assertEqual(self.label.get_languages_display(), 'English')
    
    def test_language_filtering(self):
        """Test filtering games by language"""
        # Create another game with only English
        game2 = Game.objects.create(
            name='English Only Game',
            description='Game in English only',
            player_count='3-4',
            duration='15min',
            created_by=self.user
        )
        game2.languages.add(self.english)
        
        # Test filtering by English (should return both games)
        english_games = Game.objects.filter(languages=self.english)
        self.assertEqual(english_games.count(), 2)
        
        # Test filtering by German (should return only the first game)
        german_games = Game.objects.filter(languages=self.german)
        self.assertEqual(german_games.count(), 1)
        self.assertEqual(german_games.first(), self.game)
    
    def test_language_related_names(self):
        """Test that related names work correctly"""
        # Test that we can get games from language
        english_games = self.english.games.all()
        self.assertEqual(english_games.count(), 1)
        self.assertEqual(english_games.first(), self.game)
        
        # Test that we can get focus areas from language
        english_focus = self.english.focus_areas.all()
        self.assertEqual(english_focus.count(), 1)
        self.assertEqual(english_focus.first(), self.focus)
        
        # Test that we can get materials from language
        english_materials = self.english.materials.all()
        self.assertEqual(english_materials.count(), 1)
        self.assertEqual(english_materials.first(), self.material) 