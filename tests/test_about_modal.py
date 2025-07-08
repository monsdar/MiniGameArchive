from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import AboutContent


class AboutModalTest(TestCase):
    """Test the About modal functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create sample AboutContent
        self.about_content = AboutContent.objects.create(
            title='Test Custom Section',
            content='**Bold text** and *italic text* with a [link](http://example.com)',
            is_active=True,
            order=1
        )
    
    def test_about_button_in_navigation(self):
        """Test that the About button appears in the navigation"""
        # Test as anonymous user
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertContains(response, 'data-bs-target="#aboutModal"')
        
        # Test as authenticated user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertContains(response, 'data-bs-target="#aboutModal"')
    
    def test_about_modal_content(self):
        """Test that the About modal contains expected content"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for modal structure
        self.assertContains(response, 'id="aboutModal"')
        self.assertContains(response, 'About MiniGameArchive')
        
        # Check for key features
        self.assertContains(response, 'Key Features')
        self.assertContains(response, 'Game Discovery')
        self.assertContains(response, 'Smart Filtering')
        self.assertContains(response, 'Session Planning')
        self.assertContains(response, 'Print Support')
        self.assertContains(response, 'Multilingual')
        self.assertContains(response, 'Game Suggestions')
        
        # Check for technical details
        self.assertContains(response, 'Technical Details')
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Bootstrap 5')
        
        # Check for close button
        self.assertContains(response, 'Close')
    
    def test_custom_about_content_display(self):
        """Test that custom AboutContent is displayed in the modal"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for custom content
        self.assertContains(response, 'Test Custom Section')
        self.assertContains(response, 'Bold text')
        self.assertContains(response, 'italic text')
    
    def test_about_content_markdown_rendering(self):
        """Test that markdown content is properly rendered"""
        # Create content with markdown
        markdown_content = AboutContent.objects.create(
            title='Markdown Test',
            content='**Bold** *italic* `code` and [link](http://example.com)',
            is_active=True,
            order=2
        )
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that markdown is rendered as HTML
        self.assertContains(response, '<strong>Bold</strong>')
        self.assertContains(response, '<em>italic</em>')
        self.assertContains(response, '<code>code</code>')
        self.assertContains(response, '<a href="http://example.com">link</a>')
    
    def test_about_content_links(self):
        """Test that links in markdown content are properly rendered"""
        # Create content with various types of links
        link_content = AboutContent.objects.create(
            title='Link Test',
            content='Visit our [website](https://example.com) or contact us at [email@example.com](mailto:email@example.com). Check out our [documentation](https://docs.example.com "Documentation") for more info.',
            is_active=True,
            order=3
        )
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that links are rendered as HTML
        self.assertContains(response, '<a href="https://example.com">website</a>')
        self.assertContains(response, '<a href="mailto:email@example.com">email@example.com</a>')
        self.assertContains(response, '<a href="https://docs.example.com" title="Documentation">documentation</a>')
    
    def test_inactive_about_content_not_displayed(self):
        """Test that inactive AboutContent is not displayed"""
        # Create inactive content
        inactive_content = AboutContent.objects.create(
            title='Inactive Content',
            content='This should not be displayed',
            is_active=False,
            order=3
        )
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that inactive content is not displayed
        self.assertNotContains(response, 'Inactive Content')
        self.assertNotContains(response, 'This should not be displayed')
    
    def test_about_content_ordering(self):
        """Test that AboutContent is displayed in correct order"""
        # Create content with different order
        first_content = AboutContent.objects.create(
            title='First Content',
            content='First content',
            is_active=True,
            order=1
        )
        second_content = AboutContent.objects.create(
            title='Second Content',
            content='Second content',
            is_active=True,
            order=2
        )
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Get the response content
        content = response.content.decode()
        
        # Find positions of the content
        first_pos = content.find('First Content')
        second_pos = content.find('Second Content')
        
        # First content should appear before second content
        self.assertLess(first_pos, second_pos)
    
    def test_fallback_to_default_content(self):
        """Test that default content is shown when no custom content exists"""
        # Delete all AboutContent
        AboutContent.objects.all().delete()
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for default "How to Use" section
        self.assertContains(response, 'How to Use')
        self.assertContains(response, 'Browse games using the search and filter options')
    
    def test_about_modal_translations(self):
        """Test that the About modal supports translations"""
        # Test English (default)
        response = self.client.get(reverse('game_list'))
        self.assertContains(response, 'About MiniGameArchive')
        self.assertContains(response, 'Key Features')
        
        # Test German translation
        response = self.client.get(reverse('game_list'), HTTP_ACCEPT_LANGUAGE='de')
        # Note: The actual translation would depend on the user's language setting
        # This test verifies the structure is in place for translations
        self.assertContains(response, 'About')
    
    def test_about_button_accessibility(self):
        """Test that the About button has proper accessibility attributes"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for proper button attributes
        self.assertContains(response, 'type="button"')
        self.assertContains(response, 'data-bs-toggle="modal"')
        self.assertContains(response, 'data-bs-target="#aboutModal"')
        
        # Check for icon
        self.assertContains(response, 'bi-info-circle')
    
    def test_modal_structure(self):
        """Test that the modal has proper Bootstrap structure"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for modal classes
        self.assertContains(response, 'modal fade')
        self.assertContains(response, 'modal-dialog modal-lg')
        self.assertContains(response, 'modal-content')
        self.assertContains(response, 'modal-header')
        self.assertContains(response, 'modal-body')
        self.assertContains(response, 'modal-footer')
        
        # Check for proper ARIA attributes
        self.assertContains(response, 'aria-labelledby="aboutModalLabel"')
        self.assertContains(response, 'aria-hidden="true"')
    
    def test_about_content_css_classes(self):
        """Test that AboutContent has proper CSS classes for styling"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for CSS classes
        self.assertContains(response, 'about-content')
        self.assertContains(response, 'text-primary') 