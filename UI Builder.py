#!/usr/bin/env python3
"""
Ansari Email Builder - Streamlit Prototype (Improved)
Visual interface for creating Ansari newsletters without editing YAML
"""

import streamlit as st
import yaml
from datetime import datetime
from utils.newsletter_builder import build_newsletter_from_config, DEFAULT_ICONS, PLATFORM_ICONS


# Page configuration
st.set_page_config(
    page_title="UI Builder - Ansari Email Builder",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add logo to the app
st.logo(
    image="assets/email_closed_icon.svg",
    icon_image="assets/email_opened_icon.svg",
    size="large"
)


def main():
    st.title("📧🛠️ Ansari Email Builder")
    st.markdown("Create professional newsletters with a visual interface - no code editing required!")

    # Help information - 50% width on left side
    col_info, col_empty = st.columns([1, 1])
    with col_info:
        with st.expander("ℹ️ Help & Information"):
            st.info("📌 **Icon Compatibility**: For maximum email client compatibility (Gmail, Outlook, etc.), icons should be hosted on reliable services. We currently use Google Drive. View available icons: [Ansari Icons Folder](https://drive.google.com/drive/folders/1zwTq1AJ-WrSC9tZxyFbSAgjHel4nJv6d?usp=sharing)")
            st.info("✍️ **Text Formatting**: You can use markdown notation in any text field for formatting (e.g., **bold**, *italic*, [links](https://ansari.chat)). This will render properly in the newsletter!")

    st.markdown("---")

    # Initialize session state
    if 'newsletter_config' not in st.session_state:
        st.session_state.newsletter_config = {
            'newsletter': {
                'title': 'Ansari Update',
                'greeting': 'Assalamu alaikum wa rahmatullahi wa barakatuh!',
                'unsubscribe_text': 'You are receiving this e-mail because you signed up to the Ansari updates mailing list, or because you have created an account on ansari.chat. Feel free to',
                'unsubscribe_link': 'https://chat.us21.list-manage.com/unsubscribe?u=6a15c921d5877515bdc472d7c&id=086ac2ad2d&t=b&e=%5BUNIQID%5D&c=46443b1900'
            },
            'branding': {
                'logo_url': 'https://drive.google.com/thumbnail?id=1c_R39pQEorZ3w_1uC9Z8l2_O5YzDPso2&sz=w200-h200',
                'logo_alt': 'Ansari Logo'
            },
            'highlights': {
                'title': 'In this edition:',
                'icon': DEFAULT_ICONS['highlights'],
                'highlights_list': []
            },
            'sections': [],
            'footer': {
                'signature_text': 'Remember us and Ansari in your dua!',
                'signature_icon': 'https://drive.google.com/thumbnail?id=1Ms7IhnyemP_iP2j_wIwmH0EuuZuomO94',
                'signature_icon_alt': 'Praying hands icon',
                'team_name': 'The Ansari Team'
            }
        }

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Newsletter Builder")

        # Use tabs instead of expanders
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Basic Info", "✨ Highlights", "📑 Content", "🌐 Preview"])

        with tab1:
            st.session_state.newsletter_config['newsletter']['title'] = st.text_input(
                "Newsletter Title",
                value=st.session_state.newsletter_config['newsletter']['title']
            )

            st.session_state.newsletter_config['newsletter']['greeting'] = st.text_input(
                "Greeting",
                value=st.session_state.newsletter_config['newsletter']['greeting']
            )

            st.session_state.newsletter_config['branding']['logo_url'] = st.text_input(
                "Logo URL",
                value=st.session_state.newsletter_config['branding']['logo_url']
            )

        with tab2:
            st.session_state.newsletter_config['highlights']['title'] = st.text_input(
                "Highlights Title",
                value=st.session_state.newsletter_config['highlights']['title']
            )

            st.session_state.newsletter_config['highlights']['icon'] = st.text_input(
                "Highlights Icon URL",
                value=st.session_state.newsletter_config['highlights']['icon']
            )

            st.markdown("**Highlight Items**")

            # Add new highlight
            new_highlight = st.text_input("Add new highlight (you can use markdown notation for text formatting):", key="new_highlight")
            if st.button("+ Add Highlight") and new_highlight:
                st.session_state.newsletter_config['highlights']['highlights_list'].append(new_highlight)
                st.rerun()

            # Show existing highlights with delete buttons
            highlights_to_remove = []
            for i, highlight in enumerate(st.session_state.newsletter_config['highlights']['highlights_list']):
                col_text, col_del = st.columns([4, 1])
                with col_text:
                    updated_highlight = st.text_input(f"Highlight {i+1}", value=highlight, key=f"highlight_{i}")
                    st.session_state.newsletter_config['highlights']['highlights_list'][i] = updated_highlight
                with col_del:
                    if st.button("🗑️", key=f"del_highlight_{i}", help="Delete this highlight"):
                        highlights_to_remove.append(i)

            # Remove highlights
            for i in reversed(highlights_to_remove):
                st.session_state.newsletter_config['highlights']['highlights_list'].pop(i)
                st.rerun()

        with tab3:
            # Content Sections
            st.markdown("### Add New Section")

            # Add new section
            section_type = st.selectbox(
                "Section Type:",
                ["", "content", "features", "platforms", "contributors", "feedback"],
                format_func=lambda x: {
                    "": "Select section type...",
                    "content": "📄 Text Content",
                    "features": "⭐ Feature Grid",
                    "platforms": "📱 Platform Cards",
                    "contributors": "👥 Contributors",
                    "feedback": "💬 Feedback/Contact"
                }[x]
            )

            if st.button("+ Add Section") and section_type:
                new_section = {
                    'type': section_type,
                    'title': f'{section_type.title()} Sec.',
                    'icon': DEFAULT_ICONS.get(section_type, DEFAULT_ICONS['content'])
                }

                if section_type == 'content':
                    new_section['paragraphs'] = ['Enter your content here...']
                elif section_type == 'features':
                    new_section['description'] = 'Here are the key features:'
                    new_section['features'] = [{'title': 'Feature Title', 'description': 'Feature description...'}]
                elif section_type == 'platforms':
                    new_section['description'] = 'Available on these platforms:'
                    new_section['platforms'] = [{
                        'name': 'Web',
                        'link': 'https://ansari.chat',
                        'link_text': 'ansari.chat',
                        'icon': PLATFORM_ICONS['Web']
                    }]
                    new_section['footer_text'] = []
                elif section_type == 'contributors':
                    new_section['description'] = 'We thank the following contributors:'
                    new_section['contributors'] = [{
                        'name': 'Contributor Name',
                        'description': 'Contributor description...'
                    }]
                    new_section['additional_thanks'] = []
                elif section_type == 'feedback':
                    new_section.update({
                        'paragraphs': ['We would love to hear from you!'],
                        'contact_intro': 'How to reach us:',
                        'contact_methods': [{
                            'type': 'email',
                            'text': 'Email: feedback@ansari.chat',
                            'link': 'mailto:feedback@ansari.chat'
                        }],
                        'closing_text': 'Thank you for your feedback!'
                    })

                st.session_state.newsletter_config['sections'].append(new_section)
                st.rerun()

            # Dynamic tabs for existing sections
            if st.session_state.newsletter_config['sections']:
                # Create dynamic tab names based on section titles
                section_tab_names = []
                for i, section in enumerate(st.session_state.newsletter_config['sections']):
                    section_type_emoji = {
                        'content': '📄',
                        'features': '⭐',
                        'platforms': '📱',
                        'contributors': '👥',
                        'feedback': '💬'
                    }.get(section['type'], '📄')
                    section_tab_names.append(f"{section_type_emoji} {section['title'][:20]}{'...' if len(section['title']) > 20 else ''}")

                # Create dynamic tabs for sections
                section_tabs = st.tabs(section_tab_names)
                sections_to_remove = []

                for i, (section_tab, section) in enumerate(zip(section_tabs, st.session_state.newsletter_config['sections'])):
                    with section_tab:
                        # Section delete button at top
                        if st.button("🗑️ Delete Section", key=f"remove_section_{i}", help="Delete this entire section"):
                            sections_to_remove.append(i)

                        # Section title and icon
                        section['title'] = st.text_input("Section Title", value=section['title'], key=f"section_title_{i}")
                        section['icon'] = st.text_input("Icon URL", value=section.get('icon', ''), key=f"section_icon_{i}")

                        if section['type'] == 'content':
                            if 'paragraphs' not in section:
                                section['paragraphs'] = []

                            st.markdown("**Paragraphs**")
                            paras_to_remove = []
                            for j, para in enumerate(section['paragraphs']):
                                col_para, col_del_para = st.columns([4, 1])
                                with col_para:
                                    section['paragraphs'][j] = st.text_area(f"Paragraph {j+1}", value=para, key=f"para_{i}_{j}")
                                with col_del_para:
                                    if st.button("🗑️", key=f"del_para_{i}_{j}", help="Delete this paragraph"):
                                        paras_to_remove.append(j)

                            # Remove paragraphs
                            for j in reversed(paras_to_remove):
                                section['paragraphs'].pop(j)
                                st.rerun()

                            if st.button("+ Add Paragraph", key=f"add_para_{i}"):
                                section['paragraphs'].append("New paragraph...")
                                st.rerun()

                        elif section['type'] == 'features':
                            if 'features' not in section:
                                section['features'] = []

                            section['description'] = st.text_area("Section Description", value=section.get('description', ''), key=f"feat_desc_{i}")

                            st.markdown("**Features**")
                            features_to_remove = []
                            for j, feature in enumerate(section['features']):
                                col_feat, col_del_feat = st.columns([4, 1])
                                with col_feat:
                                    feature['title'] = st.text_input(f"Feature Title {j+1}", value=feature['title'], key=f"feat_title_{i}_{j}")
                                    feature['description'] = st.text_area(f"Feature Description {j+1}", value=feature['description'], key=f"feat_content_{i}_{j}")
                                with col_del_feat:
                                    if st.button("🗑️", key=f"del_feat_{i}_{j}", help="Delete this feature"):
                                        features_to_remove.append(j)

                            # Remove features
                            for j in reversed(features_to_remove):
                                section['features'].pop(j)
                                st.rerun()

                            if st.button("+ Add Feature", key=f"add_feat_{i}"):
                                section['features'].append({'title': 'New Feature', 'description': 'Description...'})
                                st.rerun()

                        elif section['type'] == 'platforms':
                            if 'platforms' not in section:
                                section['platforms'] = []

                            section['description'] = st.text_area("Section Description", value=section.get('description', ''), key=f"plat_desc_{i}")

                            st.markdown("**Platforms**")
                            platforms_to_remove = []
                            for j, platform in enumerate(section['platforms']):
                                col_plat, col_del_plat = st.columns([4, 1])
                                with col_plat:
                                    platform['name'] = st.text_input(f"Platform Name {j+1}", value=platform['name'], key=f"plat_name_{i}_{j}")
                                    platform['link'] = st.text_input(f"Platform Link {j+1}", value=platform['link'], key=f"plat_link_{i}_{j}")
                                    platform['link_text'] = st.text_input(f"Link Text {j+1}", value=platform['link_text'], key=f"plat_text_{i}_{j}")
                                    platform['icon'] = st.text_input(f"Platform Icon {j+1}", value=platform['icon'], key=f"plat_icon_{i}_{j}")
                                with col_del_plat:
                                    if st.button("🗑️", key=f"del_plat_{i}_{j}", help="Delete this platform"):
                                        platforms_to_remove.append(j)

                            # Remove platforms
                            for j in reversed(platforms_to_remove):
                                section['platforms'].pop(j)
                                st.rerun()

                            if st.button("+ Add Platform", key=f"add_plat_{i}"):
                                section['platforms'].append({
                                    'name': 'New Platform',
                                    'link': 'https://example.com',
                                    'link_text': 'example.com',
                                    'icon': DEFAULT_ICONS['platforms']
                                })
                                st.rerun()

                        elif section['type'] == 'contributors':
                            if 'contributors' not in section:
                                section['contributors'] = []

                            section['description'] = st.text_area("Section Description", value=section.get('description', ''), key=f"contrib_desc_{i}")

                            st.markdown("**Contributors**")
                            contributors_to_remove = []
                            for j, contributor in enumerate(section['contributors']):
                                col_contrib, col_del_contrib = st.columns([4, 1])
                                with col_contrib:
                                    contributor['name'] = st.text_input(f"Contributor Name {j+1}", value=contributor['name'], key=f"contrib_name_{i}_{j}")
                                    contributor['description'] = st.text_area(f"Contributor Description {j+1}", value=contributor['description'], key=f"contrib_desc_content_{i}_{j}")
                                with col_del_contrib:
                                    if st.button("🗑️", key=f"del_contrib_{i}_{j}", help="Delete this contributor"):
                                        contributors_to_remove.append(j)

                            # Remove contributors
                            for j in reversed(contributors_to_remove):
                                section['contributors'].pop(j)
                                st.rerun()

                            if st.button("+ Add Contributor", key=f"add_contrib_{i}"):
                                section['contributors'].append({
                                    'name': 'Contributor Name',
                                    'description': 'Contributor description...'
                                })
                                st.rerun()

                            st.markdown("**Additional Thanks**")
                            if 'additional_thanks' not in section:
                                section['additional_thanks'] = []

                            thanks_to_remove = []
                            for j, thanks in enumerate(section['additional_thanks']):
                                col_thanks, col_del_thanks = st.columns([4, 1])
                                with col_thanks:
                                    section['additional_thanks'][j] = st.text_area(f"Thanks Message {j+1}", value=thanks, key=f"thanks_{i}_{j}")
                                with col_del_thanks:
                                    if st.button("🗑️", key=f"del_thanks_{i}_{j}", help="Delete this thanks message"):
                                        thanks_to_remove.append(j)

                            # Remove thanks messages
                            for j in reversed(thanks_to_remove):
                                section['additional_thanks'].pop(j)
                                st.rerun()

                            if st.button("+ Add Thanks Message", key=f"add_thanks_{i}"):
                                section['additional_thanks'].append("Thank you for your contribution!")
                                st.rerun()

                        elif section['type'] == 'feedback':
                            if 'paragraphs' not in section:
                                section['paragraphs'] = []

                            st.markdown("**Paragraphs**")
                            paras_to_remove = []
                            for j, para in enumerate(section['paragraphs']):
                                col_para, col_del_para = st.columns([4, 1])
                                with col_para:
                                    section['paragraphs'][j] = st.text_area(f"Paragraph {j+1}", value=para, key=f"feedback_para_{i}_{j}")
                                with col_del_para:
                                    if st.button("🗑️", key=f"del_feedback_para_{i}_{j}", help="Delete this paragraph"):
                                        paras_to_remove.append(j)

                            # Remove paragraphs
                            for j in reversed(paras_to_remove):
                                section['paragraphs'].pop(j)
                                st.rerun()

                            if st.button("+ Add Paragraph", key=f"add_feedback_para_{i}"):
                                section['paragraphs'].append("New paragraph...")
                                st.rerun()

                            st.markdown("**Contact Information**")
                            section['contact_intro'] = st.text_input("Contact Intro Text", value=section.get('contact_intro', 'How to reach us:'), key=f"contact_intro_{i}")

                            st.markdown("**Contact Methods/Buttons**")
                            if 'contact_methods' not in section:
                                section['contact_methods'] = []

                            contacts_to_remove = []
                            for j, contact in enumerate(section['contact_methods']):
                                col_contact, col_del_contact = st.columns([4, 1])
                                with col_contact:
                                    contact['text'] = st.text_input(f"Button Text {j+1}", value=contact.get('text', 'Email: feedback@ansari.chat'), key=f"contact_text_{i}_{j}")
                                    contact['link'] = st.text_input(f"Button Link {j+1}", value=contact.get('link', 'mailto:feedback@ansari.chat'), key=f"contact_link_{i}_{j}")
                                with col_del_contact:
                                    if st.button("🗑️", key=f"del_contact_{i}_{j}", help="Delete this contact method"):
                                        contacts_to_remove.append(j)

                            # Remove contact methods
                            for j in reversed(contacts_to_remove):
                                section['contact_methods'].pop(j)
                                st.rerun()

                            if st.button("+ Add Contact Method", key=f"add_contact_{i}"):
                                section['contact_methods'].append({
                                    'type': 'email',
                                    'text': 'Email: feedback@ansari.chat',
                                    'link': 'mailto:feedback@ansari.chat'
                                })
                                st.rerun()

                            section['closing_text'] = st.text_area("Closing Text", value=section.get('closing_text', 'Thank you for your feedback!'), key=f"closing_text_{i}")

                # Remove sections
                for i in reversed(sections_to_remove):
                    st.session_state.newsletter_config['sections'].pop(i)
                    st.rerun()
            else:
                st.info("No sections added yet. Add a section above to start editing content.")

        with tab4:
            # This will show the preview (handled in col2)
            st.markdown("The preview is shown in the right column. :)")

    with col2:
        st.header("🌐 Live Preview")

        # Build and display newsletter
        html_content, error = build_newsletter_from_config(st.session_state.newsletter_config)

        if error:
            st.error(f"Error building newsletter: {error}")
        else:
            # Display preview in an iframe-like container
            # This prevents Streamlit media file storage issues with external images
            st.components.v1.html(html_content, height=800, scrolling=True)

            # Export options
            st.markdown("### 📥 Export Options")

            col_download, col_yaml = st.columns(2)

            with col_download:
                # Download HTML
                html_bytes = html_content.encode('utf-8')
                st.download_button(
                    label="📄 Download HTML",
                    data=html_bytes,
                    file_name=f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )

            with col_yaml:
                # Download YAML config
                yaml_content = yaml.dump(st.session_state.newsletter_config, default_flow_style=False, allow_unicode=True)
                st.download_button(
                    label="📝 Download YAML",
                    data=yaml_content.encode('utf-8'),
                    file_name=f"newsletter_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml",
                    mime="text/yaml"
                )

if __name__ == "__main__":
    main()