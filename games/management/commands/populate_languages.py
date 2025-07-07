from django.core.management.base import BaseCommand
from games.models import Language


class Command(BaseCommand):
    help = 'Populate the Language model with default languages'

    def handle(self, *args, **options):
        languages = [
            {'code': 'en', 'name': 'English'},
            {'code': 'de', 'name': 'Deutsch'},
        ]
        
        created_count = 0
        for lang_data in languages:
            language, created = Language.objects.get_or_create(
                code=lang_data['code'],
                defaults={'name': lang_data['name']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created language: {language.name} ({language.code})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Language already exists: {language.name} ({language.code})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(languages)} languages. Created {created_count} new languages.')
        ) 