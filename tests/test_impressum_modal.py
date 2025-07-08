from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import ImpressumContent


class ImpressumModalTest(TestCase):
    """Test the Impressum modal functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create sample Impressum content
        self.impressum_content = ImpressumContent.objects.create(
            title='Test Impressum Section',
            content='This is a test section for the Impressum modal.',
            is_active=True,
            order=1
        )
    
    def test_impressum_link_in_footer(self):
        """Test that the Impressum link appears in the footer"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Impressum')
        self.assertContains(response, 'data-bs-target="#impressumModal"')
    
    def test_impressum_modal_structure(self):
        """Test that the Impressum modal has the correct structure"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for modal structure
        self.assertContains(response, 'id="impressumModal"')
        self.assertContains(response, 'impressumModalLabel')
        self.assertContains(response, 'impressum-modal')
    
    def test_impressum_content_display(self):
        """Test that Impressum content is displayed in the modal"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for custom content
        self.assertContains(response, 'Test Impressum Section')
        self.assertContains(response, 'This is a test section for the Impressum modal.')
    
    def test_impressum_content_context(self):
        """Test that Impressum content is available in template context"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that impressum_content is in context
        self.assertIn('impressum_content', response.context)
        impressum_content = response.context['impressum_content']
        self.assertEqual(len(impressum_content), 1)
        self.assertEqual(impressum_content[0].title, 'Test Impressum Section')
    
    def test_impressum_content_inactive(self):
        """Test that inactive Impressum content is not displayed"""
        # Make content inactive
        self.impressum_content.is_active = False
        self.impressum_content.save()
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that content is not displayed
        self.assertNotContains(response, 'Test Impressum Section')
    
    def test_impressum_content_order(self):
        """Test that Impressum content is displayed in correct order"""
        # Create another content item with higher order
        ImpressumContent.objects.create(
            title='Second Section',
            content='This is the second section.',
            is_active=True,
            order=2
        )
        
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that content is in correct order
        impressum_content = response.context['impressum_content']
        self.assertEqual(len(impressum_content), 2)
        self.assertEqual(impressum_content[0].title, 'Test Impressum Section')
        self.assertEqual(impressum_content[1].title, 'Second Section')
    
    def test_impressum_modal_translations(self):
        """Test that Impressum modal has proper translations"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for key translation strings
        self.assertContains(response, 'Publisher Information')
        self.assertContains(response, 'Contact Information')
        self.assertContains(response, 'Content Responsibility')
        self.assertContains(response, 'External Links')
        self.assertContains(response, 'Copyright')
        self.assertContains(response, 'Legal Information')
    
    def test_impressum_modal_css_classes(self):
        """Test that Impressum modal has proper CSS classes"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for CSS classes
        self.assertContains(response, 'impressum-modal')
        self.assertContains(response, 'impressum-content')
    
    def test_impressum_link_accessibility(self):
        """Test that Impressum link is accessible"""
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check for proper link attributes
        self.assertContains(response, 'href="#"')
        self.assertContains(response, 'data-bs-toggle="modal"')
        self.assertContains(response, 'data-bs-target="#impressumModal"') 