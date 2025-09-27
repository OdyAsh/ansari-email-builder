#!/usr/bin/env python3
"""
YAML Upload Page - Upload YAML configuration and generate HTML with live code editor
"""

import streamlit as st
import yaml
import traceback
import logging
from pathlib import Path
import sys
from datetime import datetime
from code_editor import code_editor
from utils.newsletter_builder import build_newsletter_from_config

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="YAML Builder - Ansari Email Builder",
    page_icon="📤",
    layout="wide"
)

# Add logo to the app
st.logo(
    image="assets/email_closed_icon.svg",
    icon_image="assets/email_opened_icon.svg",
    size="large"
)

def show_yaml_instructions():
    """Show instructions on YAML structure and visual mapping"""
    with st.expander("📖 YAML Structure & Visual Mapping Guide"):
        st.markdown("""
        ### 🗂️ YAML Configuration Structure

        The YAML file contains your email template configuration. Each section translates to specific visual elements:

        #### **📧 Newsletter Basics**
        ```yaml
        newsletter:
          title: "Your Newsletter Title"          # → Large header text
          greeting: "Welcome message"             # → Italic text below title
          unsubscribe_text: "Unsubscribe text"   # → Footer unsubscribe line
          unsubscribe_link: "https://..."        # → Unsubscribe link URL
        ```

        #### **🎨 Branding**
        ```yaml
        branding:
          logo_url: "https://..."     # → Logo image at top
          logo_alt: "Logo alt text"   # → Logo accessibility text
        ```

        #### **✨ Highlights Section**
        ```yaml
        highlights:
          title: "In this edition:"         # → Section header
          icon: "https://icon-url"           # → Header icon (32x32px)
          highlights_list:                   # → Bulleted list items
            - "First highlight **with bold**"
            - "Second highlight with [link](https://...)"
        ```

        #### **📑 Dynamic Sections**
        Each section type creates different visual layouts:

        **📄 Content Section:**
        ```yaml
        sections:
          - type: "content"
            title: "Section Title"          # → Green header with icon
            icon: "https://icon-url"        # → 32x32px icon
            paragraphs:                     # → Text paragraphs
              - "First paragraph with **formatting**"
              - "Second paragraph with [links](https://...)"
        ```

        **⭐ Features Section:**
        ```yaml
          - type: "features"
            title: "Features"
            description: "Feature intro text"
            features:                       # → Grid of feature cards
              - title: "Feature Name"       # → Blue card titles
                description: "What it does" # → Card descriptions
        ```

        **📱 Platforms Section:**
        ```yaml
          - type: "platforms"
            title: "Available On"
            platforms:                      # → Platform cards with icons
              - name: "Web"                 # → Platform name
                link: "https://..."         # → Click destination
                link_text: "Visit Site"     # → Link text
                icon: "https://icon-url"    # → Platform icon
        ```

        **👥 Contributors Section:**
        ```yaml
          - type: "contributors"
            title: "Contributors"
            contributors:                   # → Contributor cards
              - name: "John Doe"            # → Bold name
                description: "Contribution" # → Description text
            additional_thanks:              # → Additional thank you messages
              - "Thanks to everyone!"
        ```

        **💬 Feedback Section:**
        ```yaml
          - type: "feedback"
            title: "Feedback"
            paragraphs:                     # → Introduction paragraphs
              - "We'd love your feedback!"
            contact_intro: "Contact us:"    # → Contact introduction
            contact_methods:                # → Colored contact buttons
              - text: "Email Us"           # → Button text
                link: "mailto:..."          # → Button link
            closing_text: "Thank you!"      # → Closing message
        ```

        **🔢 Numbered List Section:**
        ```yaml
          - type: "numbered_list"
            title: "How You Can Help"
            description: "Optional intro text" # → Optional description paragraph
            list_items:                     # → Numbered list items
              - "First action item with **formatting**"
              - "Second item with [links](https://...)"
              - "Third action item"
        ```

        #### **🦶 Footer**
        ```yaml
        footer:
          signature_text: "Remember us in your dua!" # → Italic signature
          signature_icon: "https://icon-url"          # → Small signature icon
          signature_icon_alt: "Icon description"     # → Icon alt text
          team_name: "The Ansari Team"               # → Footer team name
        ```

        ### 🎯 **Advantages of YAML Configuration:**

        ✅ **Version Control**: Store your email templates as code in Git

        ✅ **Backup & Recovery**: Easy to backup and restore template configurations

        ✅ **Template Reuse**: Save successful layouts as template files

        ✅ **Batch Processing**: Generate multiple newsletters from different YAML files

        ✅ **Collaboration**: Share and edit templates with your team

        ✅ **Automation**: Integrate with CI/CD pipelines for automated newsletter generation

        ### 📝 **Text Formatting Support:**
        - **Bold text**: `**your text**`
        - *Italic text*: `*your text*`
        - Links: `[link text](https://url)`
        """)

def process_yaml_content(yaml_text):
    """Process YAML text and return HTML content and error if any"""
    try:
        # Parse YAML
        yaml_content = yaml.safe_load(yaml_text)

        # Debug: log the yaml_content structure
        logger.debug(f"YAML content keys: {list(yaml_content.keys())}")
        if 'highlights' in yaml_content:
            logger.debug(f"Highlights content: {yaml_content['highlights']}")
        if 'sections' in yaml_content:
            logger.debug(f"Number of sections: {len(yaml_content['sections'])}")

        # Generate HTML
        html_content, error = build_newsletter_from_config(yaml_content)
        return html_content, error, None

    except yaml.YAMLError as e:
        error_traceback = traceback.format_exc()
        logger.error(f"YAML parsing error: {error_traceback}")
        return None, f"YAML parsing error: {e}", "yaml"

    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Unexpected error processing YAML: {error_traceback}")
        return None, f"Unexpected error: {e}", "general"

def main():
    st.title("📤 YAML Code Editor & Live Preview")
    st.markdown("Edit YAML configuration and see the newsletter HTML update in real-time!")

    # Instructions
    show_yaml_instructions()

    st.markdown("---")

    # Initialize session state for YAML content
    if 'yaml_content' not in st.session_state:
        # Default sample YAML
        st.session_state.yaml_content = """newsletter:
  title: "Ansari Update Sample"
  greeting: "Assalamu alaikum wa rahmatullahi wa barakatuh!"
  unsubscribe_text: "Feel free to"
  unsubscribe_link: "https://example.com/unsubscribe"

branding:
  logo_url: "https://drive.google.com/thumbnail?id=1c_R39pQEorZ3w_1uC9Z8l2_O5YzDPso2&sz=w200-h200"
  logo_alt: "Ansari Logo"

highlights:
  title: "In this edition:"
  icon: "https://drive.google.com/thumbnail?id=1ctrBYOjrCyIWDPHFDiUuBthUm9cyI4QI"
  highlights_list:
    - "New **feature** announcement"
    - "Community [feedback](https://ansari.chat) highlights"
    - "Technical improvements and bug fixes"

sections:
  - type: "content"
    title: "What's New"
    icon: "https://drive.google.com/thumbnail?id=1a6iXO_t84QFwUIU6Kc9cpuxKQHbViBi2"
    paragraphs:
      - "We're excited to share the latest updates from **Ansari**!"
      - "This month brings several improvements to enhance your experience."

footer:
  signature_text: "Remember us and Ansari in your dua!"
  signature_icon: "https://drive.google.com/thumbnail?id=1Ms7IhnyemP_iP2j_wIwmH0EuuZuomO94"
  signature_icon_alt: "Praying hands icon"
  team_name: "The Ansari Team"
"""

    # File upload option
    st.subheader("📁 Upload YAML File (Optional)")
    uploaded_file = st.file_uploader(
        "Choose a YAML file to load into the editor",
        type=['yaml', 'yml'],
        help="Upload your newsletter configuration YAML file to load it into the editor"
    )

    if uploaded_file is not None:
        try:
            # Load uploaded file content into session state
            st.session_state.yaml_content = uploaded_file.getvalue().decode('utf-8')
            st.success("✅ YAML file loaded into editor!")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

    st.markdown("---")

    # Create main layout: code editor on left, preview on right
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📝 YAML Code Editor")

        # Code editor
        editor_response = code_editor(
            st.session_state.yaml_content,
            lang='yaml',
            theme='monokai',
            height=[32, 33],
            allow_reset=True,
            options={"showLineNumbers": True},
            buttons=[
                {
                    "name": "Save",
                    "feather": "Save",
                    "primary": True,
                    "hasText": True,
                    "showWithIcon": True,
                    "commands": ["save-state", ["response","saved"]],
                    "response": "saved",
                    "style": {"top": "0.46rem", "right": "0.4rem"}
                }
            ],
            key="yaml_editor"
        )

        # logger.debug(f"Editor response: {editor_response}")

        # Handle save button click
        if editor_response['type'] == "saved" and len(editor_response['text']) > 0:
            st.session_state.yaml_content = editor_response['text']
            st.toast("💾 YAML configuration saved!")

    with col_right:
        st.subheader("🌐 Live Preview")

        # Process current YAML content
        html_content, error, error_type = process_yaml_content(st.session_state.yaml_content)

        if error:
            st.error(f"❌ Error: {error}")
            if error_type == "yaml":
                st.info("💡 Please check your YAML syntax. Make sure indentation is consistent and all quotes are properly closed.")
            else:
                st.info("💡 Please check your YAML structure against the guide above.")
        else:
            # Display preview
            st.components.v1.html(html_content, height=800, scrolling=True)

    # Download section below the preview
    if not error and html_content:
        st.markdown("---")

        col_download, col_info = st.columns([1, 1])

        with col_download:
            st.subheader("📥 Download Options")

            # Download HTML
            html_bytes = html_content.encode('utf-8')
            filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            st.download_button(
                label="📄 Download HTML File",
                data=html_bytes,
                file_name=filename,
                mime="text/html",
                help="Download the generated HTML newsletter file"
            )

            # Download YAML
            st.download_button(
                label="📝 Download YAML File",
                data=st.session_state.yaml_content.encode('utf-8'),
                file_name=f"newsletter_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml",
                mime="text/yaml",
                help="Download the current YAML configuration"
            )

        with col_info:
            st.subheader("📊 File Info")
            st.info(f"""
            * **HTML Filename**: {filename} ({len(html_bytes) / 1024:.1f} KB)
            * **YAML Size**: {len(st.session_state.yaml_content.encode('utf-8')) / 1024:.1f} KB
            * **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """)

    # Load sample configurations
    st.markdown("---")
    st.subheader("📚 Sample Configurations")

    col_sample1, col_sample2 = st.columns(2)

    with col_sample1:
        if st.button("📧 Load Basic Sample"):
            st.session_state.yaml_content = """newsletter:
  title: "Basic Newsletter"
  greeting: "Hello and welcome!"
  unsubscribe_text: "Feel free to"
  unsubscribe_link: "https://example.com/unsubscribe"

branding:
  logo_url: "https://drive.google.com/thumbnail?id=1c_R39pQEorZ3w_1uC9Z8l2_O5YzDPso2&sz=w200-h200"
  logo_alt: "Logo"

highlights:
  title: "Highlights:"
  icon: "https://drive.google.com/thumbnail?id=1ctrBYOjrCyIWDPHFDiUuBthUm9cyI4QI"
  highlights_list:
    - "First highlight"
    - "Second highlight"

sections:
  - type: "content"
    title: "Main Content"
    icon: "https://drive.google.com/thumbnail?id=1a6iXO_t84QFwUIU6Kc9cpuxKQHbViBi2"
    paragraphs:
      - "This is the main content of your newsletter."

footer:
  signature_text: "Thank you!"
  signature_icon: "https://drive.google.com/thumbnail?id=1Ms7IhnyemP_iP2j_wIwmH0EuuZuomO94"
  signature_icon_alt: "Icon"
  team_name: "Your Team"
"""
            st.rerun()

    with col_sample2:
        if st.button("🚀 Load Full Featured Sample"):
            # Load the full Ansari update YAML
            try:
                yaml_path = Path(__file__).parent.parent / "assets" / "ansari-update-september-2025.yaml"
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    st.session_state.yaml_content = f.read()
                st.rerun()
            except Exception as e:
                st.error(f"Could not load full sample: {e}")

if __name__ == "__main__":
    main()