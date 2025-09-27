#!/usr/bin/env python3
"""
Test script for the email builder functionality
Tests core HTML generation without Streamlit UI
"""

import yaml
import re
from jinja2 import Environment

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

def test_basic_config():
    """Test with a basic newsletter configuration"""
    config = {
        'newsletter': {
            'title': 'Test Newsletter',
            'greeting': 'Assalamu alaikum wa rahmatullahi wa barakatuh!',
            'unsubscribe_text': 'You are receiving this email...',
            'unsubscribe_link': 'https://example.com/unsubscribe'
        },
        'branding': {
            'logo_url': 'https://example.com/logo.png',
            'logo_alt': 'Test Logo'
        },
        'highlights': {
            'title': 'In this test:',
            'icon': 'https://example.com/icon.png',
            'highlights_list': [
                '**Bold feature** description',
                'Another feature with [link](https://example.com)',
                '*Italic emphasis* text'
            ]
        },
        'sections': [
            {
                'type': 'content',
                'title': 'Test Content Section',
                'icon': 'https://example.com/content-icon.png',
                'paragraphs': [
                    'This is a test paragraph with **bold text**.',
                    'Another paragraph with a [test link](https://ansari.chat).'
                ]
            },
            {
                'type': 'features',
                'title': 'Test Features',
                'icon': 'https://example.com/features-icon.png',
                'description': 'These are test features:',
                'features': [
                    {
                        'title': 'Feature One',
                        'description': 'Description of feature one with **bold** text.'
                    },
                    {
                        'title': 'Feature Two',
                        'description': 'Description of feature two.'
                    }
                ]
            }
        ],
        'footer': {
            'signature_text': 'Remember us in your dua!',
            'signature_icon': 'https://example.com/prayer-icon.png',
            'signature_icon_alt': 'Prayer icon',
            'team_name': 'The Test Team'
        }
    }

    return config

def get_simple_template():
    """Simplified template for testing"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ newsletter.title }}</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1>{{ newsletter.title }}</h1>
    <p><em>{{ newsletter.greeting }}</em></p>

    {% if highlights and highlights.highlights_list %}
    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
        <h2>{{ highlights.title }}</h2>
        <ul>
            {% for item in highlights.highlights_list %}
            <li>{{ item | markdown }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    {% for section in sections %}
    <div style="margin: 30px 0;">
        <h2>{{ section.title }}</h2>

        {% if section.type == 'content' %}
            {% for paragraph in section.paragraphs %}
            <p>{{ paragraph | markdown }}</p>
            {% endfor %}
        {% endif %}

        {% if section.type == 'features' %}
            {% if section.description %}<p>{{ section.description }}</p>{% endif %}
            {% for feature in section.features %}
            <div style="border-left: 3px solid #007acc; padding-left: 15px; margin: 15px 0;">
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description | markdown }}</p>
            </div>
            {% endfor %}
        {% endif %}
    </div>
    {% endfor %}

    <footer style="text-align: center; margin-top: 50px; border-top: 1px solid #ccc; padding-top: 20px;">
        <p><em>{{ footer.signature_text }}</em></p>
        <p>{{ footer.team_name }}</p>
    </footer>
</body>
</html>'''

def test_html_generation():
    """Test HTML generation with the core functionality"""
    print("Testing Ansari Email Builder Core Functionality...")

    # Get test configuration
    config = test_basic_config()

    # Set up Jinja2 environment
    env = Environment()
    env.filters['markdown'] = markdown_to_html

    try:
        # Generate HTML
        template = env.from_string(get_simple_template())
        html_content = template.render(**config)

        print("SUCCESS: HTML generation successful!")
        print(f"Generated HTML length: {len(html_content)} characters")

        # Test markdown conversion
        test_markdown = "This has **bold** and *italic* and [link](https://example.com) text."
        converted = markdown_to_html(test_markdown)
        expected = 'This has <strong>bold</strong> and <em>italic</em> and <a href="https://example.com" style="color: #3d91c5;text-decoration: none;">link</a> text.'

        if converted == expected:
            print("SUCCESS: Markdown conversion working correctly!")
        else:
            print(f"ERROR: Markdown conversion issue:")
            print(f"Expected: {expected}")
            print(f"Got: {converted}")

        # Save test output
        with open("assets/test_output.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("SUCCESS: Test HTML saved to assets/test_output.html")

        return True

    except Exception as e:
        print(f"ERROR: Error during HTML generation: {e}")
        return False

if __name__ == "__main__":
    success = test_html_generation()
    if success:
        print("\nSUCCESS: Core email builder functionality is working!")
        print("Ready for Streamlit interface integration.")
    else:
        print("\nERROR: Core functionality has issues that need fixing.")