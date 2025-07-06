from django.conf import settings
from django.utils import translation


def language_info(request):
    """Add language information to template context"""
    current_language = translation.get_language()
    
    # Ensure we have a valid language
    if not current_language or current_language not in dict(settings.LANGUAGES):
        current_language = settings.LANGUAGE_CODE
    
    return {
        'current_language': current_language,
        'available_languages': settings.LANGUAGES,
        'language_names': dict(settings.LANGUAGES),
    }