#!/usr/bin/env python3
"""
Newsletter Builder Utilities
Shared functions for building newsletters from configuration
"""

import re
import traceback
import logging
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

# Set up logging
logger = logging.getLogger(__name__)

# Default icon mapping from original newsletter
DEFAULT_ICONS = {
    'highlights': 'https://drive.google.com/thumbnail?id=1ctrBYOjrCyIWDPHFDiUuBthUm9cyI4QI',  # flag.png
    'content': 'https://drive.google.com/thumbnail?id=1a6iXO_t84QFwUIU6Kc9cpuxKQHbViBi2',  # informationGreen.png
    'features': 'https://drive.google.com/thumbnail?id=1-If8SVPDgHrlUliLdpkfzzDEPEKdl3v-',  # chat.png
    'platforms': 'https://drive.google.com/thumbnail?id=1AukIIHwk44vaEhFTn--8VtGzl1JYRVg9',  # paperPlaneRight.png
    'contributors': 'https://drive.google.com/thumbnail?id=1Jvbt9UInwL5ZCUa9YZUtDD3rSZkmNUT7',  # challenge.png
    'feedback': 'https://drive.google.com/thumbnail?id=1FiLz-iu0bjfqSs7YckahclBjCWFsWj8T',  # Heart-hand-shake.png
    'quiz': 'https://drive.google.com/thumbnail?id=1Udwr9g61IRTajgmYUjohRuHJCtd0MhyC',  # logo.png
}

PLATFORM_ICONS = {
    'Web': 'https://drive.google.com/thumbnail?id=1NqIg3CuP0cr-B7VIh3uJ3CsEjC2d01Sd',  # internet-svgrepo-com.png
    'WhatsApp': 'https://drive.google.com/thumbnail?id=1kNwgDE1P0EjQ_UjdFJeOlPIUUxcD1L03',  # whatsapp-svgrepo-com.png
    'Android': 'https://drive.google.com/thumbnail?id=1aGsNzoaUpHSg_guBxGhsUyk_Mc4j9NT9',  # android-svgrepo-com.png
    'iOS': 'https://drive.google.com/thumbnail?id=1-fZFuN4jyou1z0nfo93uM0aU1NFzCVtu',  # apple-ios-logo-svgrepo-com.png
}

def markdown_to_html(text):
    """Simple markdown-like conversion for basic formatting"""
    if not isinstance(text, str):
        return text

    # Convert **bold** to <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Convert [text](url) to <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3d91c5;text-decoration: none;">\1</a>', text)

    # Convert *italic* to <em>
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    return text

def get_template():
    """Load and return the HTML template from external file"""
    template_path = Path(__file__).parent.parent / "assets" / "email_template.jinja2"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def build_newsletter_from_config(config):
    """Build HTML newsletter from configuration"""
    try:
        logger.debug(f"Building newsletter with config keys: {list(config.keys())}")

        env = Environment()
        env.filters['markdown'] = markdown_to_html

        template = env.from_string(get_template())
        html_content = template.render(**config)
        return html_content, None
    except Exception as e:
        # Log the full stack trace for debugging
        error_traceback = traceback.format_exc()
        logger.error(f"Error building newsletter: {error_traceback}")

        # Also log the config structure for debugging
        logger.debug(f"Config structure when error occurred: {config}")

        return None, f"{str(e)}\n\nFull error trace logged to console. Check terminal/logs for details."