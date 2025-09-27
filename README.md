# Ansari Email Builder

<div align="center">
  <img src="assets/email_icon.png" alt="Ansari Email Builder" width="64" height="64">
  <h3>Visual Interface for Creating Ansari Newsletters</h3>
  <p>A user-friendly Streamlit application for building professional newsletters without technical knowledge</p>
</div>

## 🚀 Features

### 📝 Visual Form Builder
- **Intuitive Interface**: Edit newsletter content through user-friendly forms
- **Real-time Preview**: See changes instantly in a live HTML preview
- **No Code Required**: Perfect for team members without technical background

### 📑 Dynamic Section Types
- **📄 Text Content**: Rich paragraphs with markdown support
- **⭐ Feature Grid**: Showcase features in organized cards
- **📱 Platform Cards**: Display app availability with custom icons
- **👥 Contributors**: Highlight team members and contributors
- **💬 Feedback/Contact**: Dynamic contact methods and paragraphs

### ✨ Enhanced Features
- **Dynamic Content Management**: Add, edit, and delete content within each section type
- **Flexible Paragraph System**: Multiple customizable paragraphs in feedback and content sections
- **Dynamic Contact Methods**: Customizable contact buttons with editable text and links
- **Markdown Support**: Format text with **bold**, *italic*, and [links](https://ansari.chat)
- **Export Options**: Download HTML for distribution and YAML for configuration backup

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Dependencies
The application automatically checks and installs the following dependencies:
- `streamlit>=1.28.0` - Web application framework
- `PyYAML>=6.0` - YAML configuration parsing
- `Jinja2>=3.0` - HTML template engine
- `streamlit-ace>=0.1.1` - Advanced code editor component
- `streamlit-code-editor>=0.1.19` - Enhanced code editing features

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ansari-org/ansari-email-builder.git
   cd ansari-email-builder
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

   *Alternative: Run directly with Streamlit*
   ```bash
   streamlit run "UI Builder.py"
   ```

4. **Open in Browser**
   - Streamlit will automatically open your browser
   - Or manually go to `http://localhost:8501`

## 📖 How to Use

### 1. Basic Information Tab
- Configure newsletter title and greeting message
- Set up branding with logo URL
- All changes reflect immediately in the live preview

### 2. Highlights Tab
- Add key highlights that appear at the top of newsletters
- Use markdown formatting for emphasis
- Dynamically add/edit/remove highlight items

### 3. Content Tab
- **Add Sections**: Choose from multiple section types
- **Edit Content**: Each section type has specialized editing interfaces
- **Manage Sections**: Reorder, edit, or delete sections as needed

### 4. Preview Tab
- Real-time HTML preview updates automatically
- Export options for HTML and YAML formats
- Download ready-to-send newsletters

### 5. YAML Builder Page (Advanced Users)
- Direct YAML configuration editing with syntax highlighting
- Advanced code editor with autocomplete and validation
- Switch between visual UI and YAML editing modes
- Export and import YAML configurations

## 📋 Section Types Guide

### 📄 Text Content Sections
- Multiple editable paragraphs
- Full markdown support
- Perfect for announcements and detailed descriptions

### ⭐ Feature Grid Sections
- Add/edit/delete individual features
- Each feature has title and description
- Automatically organized in responsive grid layout

### 📱 Platform Cards Sections
- Showcase app availability across platforms
- Custom icons and links for each platform
- Professional card-based design

### 👥 Contributors Sections
- **Contributors List**: Add/edit/delete individual contributors with names and descriptions
- **Additional Thanks**: Multiple thank-you messages and acknowledgments
- **Section Description**: Customizable introduction text

### 💬 Feedback/Contact Sections
- **Dynamic Paragraphs**: Multiple customizable paragraphs instead of fixed text
- **Contact Methods**: Add/edit/delete contact buttons with custom text and links
- **Flexible Layout**: Fully customizable contact information display

## 🎨 Customization

### Markdown Support
- `**bold text**` → **bold text**
- `*italic text*` → *italic text*
- `[link text](URL)` → clickable links

### Icon Integration
- Built-in icon library with Google Drive hosted images
- Custom icon support for platforms and sections
- Consistent visual branding across all newsletters

## 🏗️ Technical Architecture

### Core Components
- **Frontend**: Streamlit for rapid prototyping and user interface
- **Templating**: Jinja2 for consistent HTML generation
- **State Management**: Streamlit session state for form persistence
- **Export System**: YAML and HTML generation for multiple use cases

### File Structure
```
ansari-email-builder/
├── run.py                     # Main application runner with dependency checks
├── UI Builder.py              # Primary Streamlit UI application
├── requirements.txt           # Python dependencies
├── pages/                     # Streamlit multi-page components
│   └── YAML Builder.py       # YAML configuration editor
├── utils/                     # Utility modules
│   ├── newsletter_builder.py # Core newsletter building logic
│   ├── test_builder.py       # Testing framework
│   └── create_icon.py        # Icon generation utility
├── assets/                    # Design assets and templates
│   ├── email_template.jinja2  # HTML email template
│   ├── email_icon.*          # Application icons (PNG, SVG, ICO)
│   ├── compositeLogo.*       # Ansari branding assets
│   └── *.svg, *.png         # Various UI icons and graphics
├── secrets/                   # Private configuration and outputs
│   └── *.html, *.md         # Generated newsletters and drafts
└── README.md                 # This documentation
```

## 🚀 Development

### Application Architecture

The application follows a modular design:

- **`run.py`**: Entry point that handles dependency checking, core functionality testing, and launches the Streamlit interface
- **`UI Builder.py`**: Main Streamlit application with visual form builder
- **`YAML Builder.py`**: Advanced YAML editor page for power users
- **`utils/newsletter_builder.py`**: Core newsletter generation engine with template processing
- **`assets/email_template.jinja2`**: HTML email template with dynamic section rendering

### Adding New Section Types

1. **Update Section Selection** in `UI Builder.py`
   ```python
   section_type = st.selectbox("Section Type:",
       ["content", "features", "platforms", "contributors", "feedback", "your_new_type"])
   ```

2. **Create Section Template**
   ```python
   elif section_type == 'your_new_type':
       new_section.update({
           'field1': 'default_value',
           'field2': []
       })
   ```

3. **Add Editing Interface**
   ```python
   elif section['type'] == 'your_new_type':
       # Add form elements for editing
   ```

4. **Update HTML Template** in `assets/email_template.jinja2`
   ```html
   {% if section.type == 'your_new_type' %}
       <!-- Your HTML template -->
   {% endif %}
   ```

### Running Tests
```bash
python utils/test_builder.py
```

### Multi-Page Application
The application now supports multiple pages:
- **UI Builder**: Visual form-based editor (main page)
- **YAML Builder**: Advanced YAML configuration editor for power users

## 🤝 Contributing

We welcome contributions to improve the Ansari Email Builder! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Ansari ecosystem. Please refer to the main Ansari project for licensing information.

## 🔗 Related Projects

- [Ansari Main Platform](https://ansari.chat) - The main Ansari chat application
- [Ansari Documentation](https://docs.ansari.chat) - Comprehensive documentation

## 🆘 Support

For questions, issues, or feature requests:

- **GitHub Issues**: Use the Issues tab in this repository
- **Community**: Join the Ansari community discussions
- **Documentation**: Check the inline help within the application

## 🏆 Acknowledgments

Built with ❤️ by the Ansari team to streamline newsletter creation and improve team collaboration.

---

<div align="center">
  <p>Made with 🚀 by the <a href="https://ansari.chat">Ansari Team</a></p>
</div>