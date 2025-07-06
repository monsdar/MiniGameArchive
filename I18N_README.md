# Internationalization (i18n) Setup

This document explains how internationalization (i18n) is set up in the MiniGameArchive project.

## Overview

The project uses Django's built-in internationalization framework to support multiple languages. Currently, the following languages are supported:

- English (en) - Default
- German (de)

## Features

### Language Selection
- Users can change their language preference using the language selector in the navigation bar
- Language preference is stored in the user's session
- The system automatically detects the user's browser language on first visit
- Fallback language is English

### Translation Scope
- **UI Elements**: Navigation, buttons, labels, messages
- **Forms**: Form labels, help text, validation messages
- **Messages**: Success/error messages, notifications
- **NOT Translated**: Database content (game names, descriptions, etc.)

## How It Works

### 1. Language Detection
- The system uses Django's `LocaleMiddleware` to detect the user's preferred language
- Browser language is used as the initial language
- Users can manually change their language preference

### 2. Translation Files
- Translation files are stored in `locale/[language_code]/LC_MESSAGES/`
- Files use the standard `.po` format
- Example: `locale/de/LC_MESSAGES/django.po` for German translations

### 3. Template Translation
- Use `{% load i18n %}` at the top of templates
- Wrap translatable text in `{% trans "text" %}` tags
- Example: `{% trans "Games" %}`

### 4. Python Code Translation
- Import: `from django.utils.translation import gettext as _`
- Wrap translatable strings: `_("text")`
- Example: `messages.success(request, _("Game added successfully!"))`

## Adding New Languages

1. **Add language to settings**:
   ```python
   LANGUAGES = [
       ('en', 'English'),
       ('de', 'Deutsch'),
       ('it', 'Italiano'),  # New language
   ]
   ```

2. **Create translation directory**:
   ```bash
   mkdir -p locale/it/LC_MESSAGES
   ```

3. **Create translation file**:
   ```bash
   # If gettext is available:
   python manage.py makemessages -l it
   
   # Or create manually:
   # locale/it/LC_MESSAGES/django.po
   ```

4. **Translate the strings** in the `.po` file

5. **Compile translations**:
   ```bash
   python manage.py compilemessages
   ```

## Development Workflow

### Adding New Translatable Strings

1. **In templates**:
   ```html
   {% trans "New string to translate" %}
   ```

2. **In Python code**:
   ```python
   from django.utils.translation import gettext as _
   message = _("New string to translate")
   ```

3. **Extract messages** (if gettext is available):
   ```bash
   python manage.py makemessages -a
   ```

4. **Translate** the new strings in the `.po` files

5. **Compile** the translations:
   ```bash
   python manage.py compilemessages
   ```

### Testing Translations

Use the test command:
```bash
python manage.py test_i18n
```

## Browser Language Detection

The system automatically detects the user's browser language and sets it as the initial language. This is handled by Django's `LocaleMiddleware` and the browser's `Accept-Language` header.

## Session-based Language Storage

User language preferences are stored in the session, which means:
- Language preference persists across browser sessions
- No database changes required
- Works for both authenticated and anonymous users

## Future Enhancements

- **Database Content Translation**: Add language fields to models for translating game content
- **User Profile Language**: Store language preference in user profile for authenticated users
- **URL-based Language**: Use URL prefixes like `/de/games/` for language-specific URLs
- **RTL Support**: Add support for right-to-left languages like Arabic

## Notes

- The admin interface is not translated (as requested)
- Database content (game names, descriptions) is not translated
- All UI elements and messages are translatable
- English is the fallback language for missing translations 