from django import template
from django.utils.safestring import mark_safe
import markdown
import bleach
import re

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert markdown text to HTML with limited allowed tags for security.
    Supports: bold, italic, underline, lists, and basic formatting. Headers are not allowed.
    """
    if not text:
        return ""

    # Remove markdown header syntax (lines starting with #)
    text = re.sub(r'^(\s{0,3}#{1,6}\s+)', '', text, flags=re.MULTILINE)

    # Configure markdown with limited extensions
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.nl2br',  # Convert newlines to <br>
            'markdown.extensions.sane_lists',  # Better list handling
        ]
    )
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Define allowed HTML tags and attributes for security (no headers)
    allowed_tags = [
        'p', 'br', 'strong', 'b', 'em', 'i', 'u',  # Basic formatting
        'ul', 'ol', 'li',  # Lists
        'blockquote',  # Blockquotes
        'code', 'pre',  # Code blocks
    ]
    
    allowed_attributes = {
        '*': ['class'],  # Allow class attribute on all elements
    }
    
    # Clean the HTML to remove potentially dangerous content
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    return mark_safe(clean_html)

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key) 