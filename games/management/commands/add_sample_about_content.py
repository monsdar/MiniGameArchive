from django.core.management.base import BaseCommand
from games.models import AboutContent


class Command(BaseCommand):
    help = 'Add sample About content for testing'

    def handle(self, *args, **options):
        # Clear existing sample content
        AboutContent.objects.filter(title__startswith='Sample').delete()
        
        # Create sample content
        sample_content = [
            {
                'title': 'Sample: Getting Started',
                'content': """**Welcome to MiniGameArchive!**

This platform helps you organize and plan your sports training sessions. Here's how to get started:

1. **Browse Games**: Use the search and filter options to find games that match your needs
2. **Add to Session**: Click "Add to Session" on any game to include it in your training plan
3. **Review & Print**: Check your session in the "Training Session" tab and print when ready

*Tip: You can filter games by focus area, player count, duration, and materials needed.*""",
                'order': 1
            },
            {
                'title': 'Sample: Custom Instructions',
                'content': """**Custom Training Guidelines**

Every coach has their own style and preferences. Here are some tips for effective training:

- **Warm-up properly** before starting any session
- **Adapt games** to your players' skill levels
- **Keep it fun** - engagement is key to learning
- **Track progress** by saving your favorite sessions

> *Remember: The best training sessions are those that challenge players while keeping them engaged and having fun.*""",
                'order': 2
            },
            {
                'title': 'Sample: Contact Information',
                'content': """**Need Help?**

If you have questions or suggestions, please contact us:

- **Email**: [coach@example.com](mailto:coach@example.com)
- **Phone**: (555) 123-4567
- **Website**: [Visit our site](https://example.com)
- **Office Hours**: Monday-Friday, 9AM-5PM

We're here to help you make the most of your training sessions! Check out our [documentation](https://docs.example.com "Training Documentation") for detailed guides.""",
                'order': 3
            }
        ]
        
        for content_data in sample_content:
            content, created = AboutContent.objects.get_or_create(
                title=content_data['title'],
                defaults={
                    'content': content_data['content'],
                    'order': content_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created sample content: "{content.title}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Sample content already exists: "{content.title}"')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Sample About content has been added successfully!')
        ) 