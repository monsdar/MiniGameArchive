from django.conf import settings
from django.utils import translation
from .models import AboutContent, ImpressumContent


def language_info(request):
    """Add language information to template context"""
    # Check session for language preference
    session_language = request.session.get('django_language')
    if session_language and session_language in dict(settings.LANGUAGES):
        # Activate the session language
        translation.activate(session_language)
        current_language = session_language
    else:
        # Use the currently active language
        current_language = translation.get_language()
        
        # Ensure we have a valid language
        if not current_language or current_language not in dict(settings.LANGUAGES):
            current_language = settings.LANGUAGE_CODE
    
    return {
        'current_language': current_language,
        'available_languages': settings.LANGUAGES,
        'language_names': dict(settings.LANGUAGES),
        'about_content': AboutContent.objects.filter(is_active=True).order_by('order', 'created_at'),
        'impressum_content': ImpressumContent.objects.filter(is_active=True).order_by('order', 'created_at'),
    }