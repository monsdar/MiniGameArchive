from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from games.models import AboutContent


class AboutContentAdminTest(TestCase):
    """Test the AboutContent admin functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create test content
        self.about_content = AboutContent.objects.create(
            title='Test Content',
            content='**Bold text** and *italic text*',
            is_active=True,
            order=1
        )
    
    def test_about_content_admin_list(self):
        """Test that AboutContent appears in admin list"""
        response = self.client.get(reverse('admin:games_aboutcontent_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        self.assertContains(response, 'Active')
    
    def test_about_content_admin_detail(self):
        """Test that AboutContent detail view works"""
        response = self.client.get(
            reverse('admin:games_aboutcontent_change', args=[self.about_content.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        self.assertContains(response, '**Bold text** and *italic text*')
    
    def test_about_content_admin_create(self):
        """Test creating new AboutContent through admin"""
        data = {
            'title': 'New Content',
            'content': 'This is **new** content with *formatting*',
            'is_active': True,
            'order': 2
        }
        
        response = self.client.post(
            reverse('admin:games_aboutcontent_add'),
            data
        )
        
        # Should redirect to changelist after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify the content was created
        new_content = AboutContent.objects.get(title='New Content')
        self.assertEqual(new_content.content, 'This is **new** content with *formatting*')
        self.assertTrue(new_content.is_active)
        self.assertEqual(new_content.order, 2)
    
    def test_about_content_admin_update(self):
        """Test updating AboutContent through admin"""
        data = {
            'title': 'Updated Content',
            'content': 'This content has been **updated**',
            'is_active': True,
            'order': 1
        }
        
        response = self.client.post(
            reverse('admin:games_aboutcontent_change', args=[self.about_content.id]),
            data
        )
        
        # Should redirect to changelist after successful update
        self.assertEqual(response.status_code, 302)
        
        # Verify the content was updated
        self.about_content.refresh_from_db()
        self.assertEqual(self.about_content.title, 'Updated Content')
        self.assertEqual(self.about_content.content, 'This content has been **updated**')
    
    def test_about_content_admin_delete(self):
        """Test deleting AboutContent through admin"""
        response = self.client.post(
            reverse('admin:games_aboutcontent_delete', args=[self.about_content.id]),
            {'post': 'yes'}
        )
        
        # Should redirect to changelist after successful deletion
        self.assertEqual(response.status_code, 302)
        
        # Verify the content was deleted
        self.assertFalse(AboutContent.objects.filter(id=self.about_content.id).exists())
    
    def test_about_content_ordering(self):
        """Test that AboutContent is ordered correctly in admin"""
        # Create content with different order
        AboutContent.objects.create(
            title='Second Content',
            content='Second content',
            is_active=True,
            order=2
        )
        
        response = self.client.get(reverse('admin:games_aboutcontent_changelist'))
        self.assertEqual(response.status_code, 200)
        
        # Get the response content
        content = response.content.decode()
        
        # Find positions of the content
        first_pos = content.find('Test Content')
        second_pos = content.find('Second Content')
        
        # First content should appear before second content (due to order)
        self.assertLess(first_pos, second_pos)
    
    def test_about_content_filtering(self):
        """Test that AboutContent admin filters work"""
        # Create inactive content
        AboutContent.objects.create(
            title='Inactive Content',
            content='Inactive content',
            is_active=False,
            order=3
        )
        
        # Test active filter
        response = self.client.get(
            reverse('admin:games_aboutcontent_changelist') + '?is_active__exact=1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        self.assertNotContains(response, 'Inactive Content')
        
        # Test inactive filter
        response = self.client.get(
            reverse('admin:games_aboutcontent_changelist') + '?is_active__exact=0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Content')
        self.assertContains(response, 'Inactive Content')
    
    def test_about_content_search(self):
        """Test that AboutContent admin search works"""
        # Search by title
        response = self.client.get(
            reverse('admin:games_aboutcontent_changelist') + '?q=Test'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        
        # Search by content
        response = self.client.get(
            reverse('admin:games_aboutcontent_changelist') + '?q=Bold'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        
        # Search for non-existent content
        response = self.client.get(
            reverse('admin:games_aboutcontent_changelist') + '?q=Nonexistent'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Content') 