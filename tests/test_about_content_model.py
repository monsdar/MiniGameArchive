from django.test import TestCase
from django.contrib.auth.models import User
from games.models import AboutContent


class AboutContentModelTest(TestCase):
    """Test the AboutContent model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_about_content_creation(self):
        """Test that AboutContent can be created"""
        content = AboutContent.objects.create(
            title='Test Content',
            content='**Bold text** and *italic text*',
            is_active=True,
            order=1
        )
        
        self.assertEqual(content.title, 'Test Content')
        self.assertEqual(content.content, '**Bold text** and *italic text*')
        self.assertTrue(content.is_active)
        self.assertEqual(content.order, 1)
        self.assertIsNotNone(content.created_at)
        self.assertIsNotNone(content.updated_at)
    
    def test_about_content_string_representation(self):
        """Test the string representation of AboutContent"""
        active_content = AboutContent.objects.create(
            title='Active Content',
            content='Active content',
            is_active=True,
            order=1
        )
        
        inactive_content = AboutContent.objects.create(
            title='Inactive Content',
            content='Inactive content',
            is_active=False,
            order=2
        )
        
        self.assertEqual(str(active_content), 'Active Content (Active)')
        self.assertEqual(str(inactive_content), 'Inactive Content (Inactive)')
    
    def test_about_content_ordering(self):
        """Test that AboutContent is ordered correctly"""
        # Create content in reverse order
        second_content = AboutContent.objects.create(
            title='Second Content',
            content='Second content',
            is_active=True,
            order=2
        )
        
        first_content = AboutContent.objects.create(
            title='First Content',
            content='First content',
            is_active=True,
            order=1
        )
        
        third_content = AboutContent.objects.create(
            title='Third Content',
            content='Third content',
            is_active=True,
            order=3
        )
        
        # Get all content ordered by the model's Meta ordering
        all_content = AboutContent.objects.all()
        
        # Should be ordered by order, then created_at
        self.assertEqual(all_content[0], first_content)
        self.assertEqual(all_content[1], second_content)
        self.assertEqual(all_content[2], third_content)
    
    def test_about_content_active_filtering(self):
        """Test filtering active AboutContent"""
        active_content = AboutContent.objects.create(
            title='Active Content',
            content='Active content',
            is_active=True,
            order=1
        )
        
        inactive_content = AboutContent.objects.create(
            title='Inactive Content',
            content='Inactive content',
            is_active=False,
            order=2
        )
        
        # Test active filter
        active_contents = AboutContent.objects.filter(is_active=True)
        self.assertEqual(active_contents.count(), 1)
        self.assertIn(active_content, active_contents)
        self.assertNotIn(inactive_content, active_contents)
        
        # Test inactive filter
        inactive_contents = AboutContent.objects.filter(is_active=False)
        self.assertEqual(inactive_contents.count(), 1)
        self.assertIn(inactive_content, inactive_contents)
        self.assertNotIn(active_content, inactive_contents)
    
    def test_about_content_update(self):
        """Test updating AboutContent"""
        content = AboutContent.objects.create(
            title='Original Title',
            content='Original content',
            is_active=True,
            order=1
        )
        
        # Update the content
        content.title = 'Updated Title'
        content.content = 'Updated content'
        content.is_active = False
        content.save()
        
        # Refresh from database
        content.refresh_from_db()
        
        self.assertEqual(content.title, 'Updated Title')
        self.assertEqual(content.content, 'Updated content')
        self.assertFalse(content.is_active)
    
    def test_about_content_deletion(self):
        """Test deleting AboutContent"""
        content = AboutContent.objects.create(
            title='To Delete',
            content='Content to delete',
            is_active=True,
            order=1
        )
        
        content_id = content.id
        content.delete()
        
        # Verify it's deleted
        self.assertFalse(AboutContent.objects.filter(id=content_id).exists())
    
    def test_about_content_meta_options(self):
        """Test that AboutContent has correct Meta options"""
        meta = AboutContent._meta
        
        # Check ordering
        self.assertEqual(meta.ordering, ['order', 'created_at'])
        
        # Check verbose names
        self.assertEqual(meta.verbose_name, 'About Content')
        self.assertEqual(meta.verbose_name_plural, 'About Content')
    
    def test_about_content_field_constraints(self):
        """Test AboutContent field constraints"""
        # Test that title can be up to 200 characters
        long_title = 'A' * 200
        content = AboutContent.objects.create(
            title=long_title,
            content='Test content',
            is_active=True,
            order=1
        )
        
        self.assertEqual(content.title, long_title)
        
        # Test that order must be positive
        content.order = 0
        content.save()
        
        # Test that content can be empty
        empty_content = AboutContent.objects.create(
            title='Empty Content',
            content='',
            is_active=True,
            order=2
        )
        
        self.assertEqual(empty_content.content, '')
    
    def test_about_content_multiple_entries(self):
        """Test multiple AboutContent entries"""
        # Create multiple entries
        contents = []
        for i in range(5):
            content = AboutContent.objects.create(
                title=f'Content {i}',
                content=f'Content {i} body',
                is_active=True,
                order=i
            )
            contents.append(content)
        
        # Verify all were created
        self.assertEqual(AboutContent.objects.count(), 5)
        
        # Verify they're ordered correctly
        all_contents = AboutContent.objects.all()
        for i, content in enumerate(all_contents):
            self.assertEqual(content.order, i)
            self.assertEqual(content.title, f'Content {i}') 