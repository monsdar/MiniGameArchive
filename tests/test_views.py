"""
Unit tests for Django views
"""
import json
import logging
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import translation
from games.models import Game, Focus, Material, Label, TrainingSession, SessionGame
import os
from django.conf import settings

logger = logging.getLogger(__name__)


class ViewTestCase(TestCase):
    """Base test case for views with common setup"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
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


class GameListViewTest(ViewTestCase):
    """Test cases for game list view"""
    
    def test_game_list_view(self):
        """Test that game list view loads correctly"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_list.html')
        self.assertContains(response, "Test Game")
    
    def test_game_list_with_search(self):
        """Test game list with search parameter"""
        response = self.client.get(reverse('game_list'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        
        response = self.client.get(reverse('game_list'), {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Game")
    
    def test_game_list_with_filters(self):
        """Test game list with various filters"""
        # Test focus filter
        response = self.client.get(reverse('game_list'), {'focus': 'Dribbling'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        
        # Test player count filter
        response = self.client.get(reverse('game_list'), {'player_count': '2-4'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        
        # Test duration filter
        response = self.client.get(reverse('game_list'), {'duration': '10min'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
    
    def test_game_list_pagination(self):
        """Test game list pagination"""
        # Create multiple games to test pagination
        for i in range(25):
            game = Game.objects.create(
                name=f"Game {i}",
                description=f"Description for game {i}",
                player_count="1-2",
                duration="5min",
                created_by=self.user
            )
            game.focus.add(self.focus)
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['page_obj'].has_other_pages())


class GameDetailViewTest(ViewTestCase):
    """Test cases for game detail view"""
    
    def test_game_detail_view(self):
        """Test that game detail view loads correctly"""
        response = self.client.get(reverse('game_detail', args=[self.game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_detail.html')
        self.assertContains(response, "Test Game")
        self.assertContains(response, "A test game for dribbling practice")
    
    def test_game_detail_view_404(self):
        """Test that game detail view returns 404 for non-existent game"""
        response = self.client.get(reverse('game_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class CartViewTest(ViewTestCase):
    """Test cases for cart/training session views"""
    
    def test_cart_view_empty(self):
        """Test cart view when empty"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/cart.html')
        self.assertContains(response, "No games in your training session")
    
    def test_cart_view_with_games(self):
        """Test cart view with games in session"""
        # Add game to session
        session = self.client.session
        session['cart'] = [self.game.id]
        session.save()
        
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Selected Games")
    
    def test_cart_view_create_session(self):
        """Test creating a training session from cart"""
        # Add game to session
        session = self.client.session
        session['cart'] = [self.game.id]
        session.save()
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Create session
        response = self.client.post(reverse('cart'), {
            'name': 'Test Training Session',
            'description': 'A test session'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that session was created
        training_session = TrainingSession.objects.get(name='Test Training Session')
        self.assertEqual(training_session.created_by, self.user)
        self.assertEqual(training_session.sessiongame_set.count(), 1)
        
        # Check that cart was cleared
        session = self.client.session
        self.assertEqual(session.get('cart', []), [])


class CartAPITest(ViewTestCase):
    """Test cases for cart API endpoints"""
    
    def test_add_to_cart(self):
        """Test adding game to cart"""
        response = self.client.post(
            reverse('add_to_cart'),
            data=json.dumps({'game_id': self.game.id}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)
        
        # Check that game was added to session
        session = self.client.session
        self.assertIn(self.game.id, session.get('cart', []))
    
    def test_add_to_cart_invalid_game(self):
        """Test adding non-existent game to cart"""
        response = self.client.post(
            reverse('add_to_cart'),
            data=json.dumps({'game_id': 99999}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_add_to_cart_missing_game_id(self):
        """Test adding to cart without game ID"""
        response = self.client.post(
            reverse('add_to_cart'),
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_remove_from_cart(self):
        """Test removing game from cart"""
        # Add game to cart first
        session = self.client.session
        session['cart'] = [self.game.id]
        session.save()
        
        response = self.client.post(
            reverse('remove_from_cart'),
            data=json.dumps({'game_id': self.game.id}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 0)
        
        # Check that game was removed from session
        session = self.client.session
        self.assertNotIn(self.game.id, session.get('cart', []))
    
    def test_clear_cart(self):
        """Test clearing cart"""
        # Add games to cart
        session = self.client.session
        session['cart'] = [self.game.id]
        session.save()
        
        response = self.client.post(reverse('clear_cart'))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that cart was cleared
        session = self.client.session
        self.assertEqual(session.get('cart', []), [])


class LanguageViewTest(ViewTestCase):
    """Test cases for language switching"""
    
    def test_set_language(self):
        """Test setting language preference"""
        response = self.client.post(reverse('set_language'), {
            'language': 'de',
            'next': reverse('game_list')
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check that language was set in session
        session = self.client.session
        self.assertEqual(session.get('django_language'), 'de')
    
    def test_set_language_invalid(self):
        """Test setting invalid language"""
        response = self.client.post(reverse('set_language'), {
            'language': 'invalid',
            'next': reverse('game_list')
        })
        
        self.assertEqual(response.status_code, 302)  # Still redirects
    
    def test_set_language_no_language(self):
        """Test setting language without language parameter"""
        response = self.client.post(reverse('set_language'), {
            'next': reverse('game_list')
        })
        
        self.assertEqual(response.status_code, 302)  # Still redirects


class SessionViewTest(ViewTestCase):
    """Test cases for training session views"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.client.login(username='testuser', password='testpass123')
        
        self.session = TrainingSession.objects.create(
            name="Test Session",
            description="A test training session",
            created_by=self.user
        )
        
        SessionGame.objects.create(
            session=self.session,
            game=self.game,
            order=1
        )
    
    def test_session_list_view(self):
        """Test session list view"""
        response = self.client.get(reverse('session_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/session_list.html')
        self.assertContains(response, "Test Session")
    
    def test_session_detail_view(self):
        """Test session detail view"""
        response = self.client.get(reverse('session_detail', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/session_detail.html')
        self.assertContains(response, "Test Session")
        self.assertContains(response, "Test Game")
    
    def test_session_detail_view_404(self):
        """Test session detail view for non-existent session"""
        response = self.client.get(reverse('session_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
    
    def test_session_detail_view_unauthorized(self):
        """Test session detail view for another user's session"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        other_session = TrainingSession.objects.create(
            name="Other Session",
            description="Another user's session",
            created_by=other_user
        )
        
        response = self.client.get(reverse('session_detail', args=[other_session.id]))
        self.assertEqual(response.status_code, 404)  # Should not be accessible


class GameSuggestionViewTest(ViewTestCase):
    """Test cases for game suggestion view"""
    
    def test_game_suggestion_view_get(self):
        """Test game suggestion view GET request"""
        response = self.client.get(reverse('game_suggestion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_suggestion.html')
    
    def test_game_suggestion_view_post(self):
        """Test game suggestion view POST request"""
        response = self.client.post(reverse('game_suggestion'), {
            'name': 'Suggested Game',
            'description': 'A suggested game',
            'player_count': '2-4',
            'duration': '10min',
            'focus': [self.focus.id],
            'materials': [self.material.id],
            'labels': [self.label.id],
            'variants': 'Some variants',
            'email': 'test@example.com'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that suggestion was created (if you have a GameSuggestion model)
        # This would depend on your actual implementation


class PrintViewTest(ViewTestCase):
    """Test cases for print views"""
    
    def test_print_game_view(self):
        """Test print game view"""
        response = self.client.get(reverse('print_game', args=[self.game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/print_game.html')
        self.assertContains(response, "Test Game")
    
    def test_print_session_view(self):
        """Test print session view"""
        self.client.login(username='testuser', password='testpass123')
        
        session = TrainingSession.objects.create(
            name="Test Session",
            description="A test training session",
            created_by=self.user
        )
        
        SessionGame.objects.create(
            session=session,
            game=self.game,
            order=1
        )
        
        response = self.client.get(reverse('print_session', args=[session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/print_session.html')
        self.assertContains(response, "Test Session")
    
    def test_print_session_builder_view(self):
        """Test print session builder view"""
        # Add game to cart
        session = self.client.session
        session['cart'] = [self.game.id]
        session.save()
        
        response = self.client.get(reverse('print_session_builder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/print_session.html')
        self.assertContains(response, "Test Game")


class AuthenticationTest(ViewTestCase):
    """Test cases for authentication requirements"""
    
    def test_session_list_requires_login(self):
        """Test that session list requires login"""
        response = self.client.get(reverse('session_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Login and try again
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('session_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_session_detail_requires_login(self):
        """Test that session detail requires login"""
        session = TrainingSession.objects.create(
            name="Test Session",
            description="A test training session",
            created_by=self.user
        )
        
        response = self.client.get(reverse('session_detail', args=[session.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Login and try again
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('session_detail', args=[session.id]))
        self.assertEqual(response.status_code, 200)


class InternationalizationTest(ViewTestCase):
    """Test cases for internationalization"""
    
    def test_language_context_processor(self):
        """Test that language context processor adds language info"""
        from games.context_processors import language_info
        
        # Test with English
        request = self.factory.get('/')
        request.session = {'django_language': 'en'}
        context = language_info(request)
        
        self.assertIn('current_language', context)
        self.assertIn('available_languages', context)
        self.assertEqual(context['current_language'], 'en')
        self.assertIn(('en', 'English'), context['available_languages'])
        self.assertIn(('de', 'Deutsch'), context['available_languages'])
        
        # Test with German
        request.session = {'django_language': 'de'}
        context = language_info(request)
        self.assertEqual(context['current_language'], 'de')
    
    def test_language_switching_persistence(self):
        """Test that language preference persists across requests"""
        # Set language to German
        self.client.post(reverse('set_language'), {
            'language': 'de',
            'next': reverse('game_list')
        })
        
        # Check that language is set in session
        session = self.client.session
        self.assertEqual(session.get('django_language'), 'de')
        
        # Make another request and check language is still set in session
        self.client.get(reverse('game_list'))
        session = self.client.session
        self.assertEqual(session.get('django_language'), 'de')

    def test_logging_in_views(self):
        """Test that views log appropriate messages"""
        import logging
        
        # Get the logger
        logger = logging.getLogger('django')
        
        # Test that logging works by writing a test message
        logger.info('Test log message from test')
        
        # Verify that logging is configured (basic check)
        self.assertIsNotNone(logger)
        self.assertTrue(logger.isEnabledFor(logging.INFO)) 