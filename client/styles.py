"""
CareCase UI Styles
-----------------
Shared style definitions for consistent UI theming across the application.
"""

# Color Palette
COLORS = {
    # Backgrounds
    "bg_primary": "#e6f0fa",      # Light blue background
    "bg_secondary": "#f8fafc",    # Very light blue-gray
    "navbar_bg": "#abd4f5",       # Slightly darker blue for navbar
    
    # Text colors
    "text_primary": "#2c3e50",    # Dark blue-gray
    "text_secondary": "#34495e",  # Medium blue-gray
    "text_light": "white",        # White text for buttons
    
    # Accent colors
    "accent_primary": "#3498db",  # Bright blue for primary actions
    "accent_hover": "#2980b9",    # Darker blue for button hover
    "accent_success": "#27ae60",  # Green for success indicators
    "accent_warning": "#f39c12",  # Orange for warning indicators
    "accent_error": "#e74c3c",    # Red for error messages
    
    # Card and UI elements
    "card_border": "#e1ebf2",     # Light blue border for cards
    "card_bg": "white",           # White background for cards
    "button_secondary": "#f0f0f0" # Light gray for secondary buttons
}

# Typography
FONTS = {
    "title": ("Helvetica", 32, "bold"),
    "subtitle": ("Helvetica", 22, "bold"),
    "body": ("Helvetica", 12),
    "body_small": ("Helvetica", 10),
    "button": ("Helvetica", 12, "bold"),
    "button_small": ("Helvetica", 10, "bold"),
    "logo": ("Helvetica", 10, "bold")
}

# Spacing
SPACING = {
    "tiny": 5,
    "small": 10,
    "medium": 15,
    "large": 20,
    "xlarge": 30
}

# UI Element Styling
BUTTON_STYLES = {
    "primary": {
        "bg": COLORS["accent_primary"],
        "fg": COLORS["text_light"],
        "activebackground": COLORS["accent_hover"],
        "activeforeground": COLORS["text_light"],
        "relief": "flat",
        "cursor": "hand2"
    },
    "secondary": {
        "bg": COLORS["button_secondary"],
        "fg": COLORS["text_secondary"],
        "activebackground": "#e0e0e0",
        "activeforeground": COLORS["text_secondary"],
        "relief": "flat",
        "cursor": "hand2"
    }
}

# Common UI Creation Functions
def create_navbar(parent, controller=None):
    """Create a consistent navbar for all pages"""
    navbar = parent.Frame(parent, bg=COLORS["navbar_bg"], height=40)
    navbar.pack(side="top", fill="x")
    
    # Logo/home button
    logo = parent.Label(
        navbar, 
        text="👩🏾‍⚕️CareCase", 
        font=FONTS["logo"], 
        bg=COLORS["navbar_bg"], 
        fg=COLORS["text_primary"]
    )
    logo.pack(side="left", padx=10)
    
    # Right-aligned elements
    help_btn = parent.ttk.Button(navbar, text="Help", width=8)
    help_btn.pack(side="right", padx=5, pady=5)
    
    # Language dropdown
    lang_var = parent.StringVar(value="English")
    lang_dropdown = parent.ttk.Combobox(navbar, textvariable=lang_var, width=10, state="readonly")
    lang_dropdown['values'] = ('English', 'Spanish', 'French')
    lang_dropdown.pack(side="right", padx=5, pady=5)
    
    # Accessibility button
    access_btn = parent.ttk.Button(navbar, text="♿", width=3)
    access_btn.pack(side="right", padx=5, pady=5)
    
    return navbar 