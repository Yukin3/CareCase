import tkinter as tk
from tkinter import ttk
import requests
from styles import COLORS, FONTS, SPACING, BUTTON_STYLES

class SelectScenarioPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_secondary"])
        self.controller = controller
        
        # Accessibility settings
        self.font_scale = 1.0
        self.high_contrast = False
        
        # Create navbar
        self.create_navbar()
        
        # Main content container
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"])
        content_frame.pack(fill="both", expand=True, padx=SPACING["large"], pady=SPACING["small"])

        # --- Header ---
        header_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        header_frame.pack(fill="x", pady=(SPACING["small"], SPACING["large"]))
        
        header = tk.Label(
            header_frame, 
            text="Choose a Scenario", 
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        header.pack(side="left")
        
        # Small icon next to header
        icon = tk.Label(
            header_frame,
            text="🩺",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        icon.pack(side="left", padx=(SPACING["small"], 0))

        # --- Scenario List in a scrollable container ---
        self.scroll_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.scroll_frame, bg=COLORS["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        
        self.scenario_container = tk.Frame(self.canvas, bg=COLORS["bg_secondary"])
        self.scenario_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scenario_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_scenarios()

        # --- Back Button in a footer frame ---
        footer = tk.Frame(content_frame, bg=COLORS["bg_secondary"], height=50)
        footer.pack(fill="x", pady=(SPACING["small"], SPACING["tiny"]))
        
        back_btn = tk.Button(
            footer, 
            text="← Back", 
            command=lambda: controller.show_frame("HomePage"),
            font=FONTS["body_small"],
            **BUTTON_STYLES["secondary"]
        )
        back_btn.config(padx=SPACING["medium"], pady=SPACING["tiny"])
        back_btn.pack(side="left", pady=SPACING["small"])

    def create_navbar(self):
        navbar = tk.Frame(self, bg=COLORS["navbar_bg"], height=40)
        navbar.pack(side="top", fill="x")
        
        # Logo/home button
        logo = tk.Label(
            navbar, 
            text="👩🏾‍⚕️CareCase", 
            font=FONTS["logo"], 
            bg=COLORS["navbar_bg"], 
            fg=COLORS["text_primary"]
        )
        logo.pack(side="left", padx=SPACING["small"])
        
        # Right-aligned elements
        help_btn = ttk.Button(navbar, text="Help", width=8)
        help_btn.pack(side="right", padx=SPACING["tiny"], pady=SPACING["tiny"])
        
        # Language dropdown
        lang_var = tk.StringVar(value="English")
        lang_dropdown = ttk.Combobox(navbar, textvariable=lang_var, width=10, state="readonly")
        lang_dropdown['values'] = ('English', 'Spanish', 'French')
        lang_dropdown.pack(side="right", padx=SPACING["tiny"], pady=SPACING["tiny"])
        
        # Accessibility button with popup function
        access_btn = ttk.Button(navbar, text="♿", width=3, command=self.show_accessibility_options)
        access_btn.pack(side="right", padx=SPACING["tiny"], pady=SPACING["tiny"])

    def show_accessibility_options(self):
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Accessibility Options")
        popup.geometry("300x200")
        popup.resizable(False, False)
        popup.transient(self)  # Set to be on top of the parent window
        popup.grab_set()  # Modal behavior
        
        # Style the popup
        popup.configure(bg=COLORS["bg_secondary"])
        
        # Title
        title = tk.Label(
            popup, 
            text="Accessibility Options",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        title.pack(pady=(15, 20))
        
        # Font size controls
        font_frame = tk.Frame(popup, bg=COLORS["bg_secondary"])
        font_frame.pack(fill="x", padx=20, pady=5)
        
        font_label = tk.Label(
            font_frame,
            text="Font Size:",
            font=FONTS["body"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        font_label.pack(side="left")
        
        increase_btn = tk.Button(
            font_frame,
            text="+ Increase",
            command=lambda: self.change_font_size(1.1),
            **BUTTON_STYLES["secondary"]
        )
        increase_btn.pack(side="right", padx=5)
        
        decrease_btn = tk.Button(
            font_frame,
            text="- Decrease",
            command=lambda: self.change_font_size(0.9),
            **BUTTON_STYLES["secondary"]
        )
        decrease_btn.pack(side="right", padx=5)
        
        # Contrast mode toggle
        contrast_frame = tk.Frame(popup, bg=COLORS["bg_secondary"])
        contrast_frame.pack(fill="x", padx=20, pady=15)
        
        contrast_label = tk.Label(
            contrast_frame,
            text="High Contrast:",
            font=FONTS["body"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        contrast_label.pack(side="left")
        
        toggle_btn = tk.Button(
            contrast_frame,
            text="Toggle On/Off",
            command=self.toggle_high_contrast,
            **BUTTON_STYLES["secondary"]
        )
        toggle_btn.pack(side="right")
        
        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            **BUTTON_STYLES["primary"]
        )
        close_btn.pack(pady=15)

    def change_font_size(self, scale_factor):
        # Update font scale
        self.font_scale *= scale_factor
        
        # Apply to all relevant widgets on the current page
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                self._scale_font(widget)
                
        # Apply to scenario container and its children
        for card in self.scenario_container.winfo_children():
            for widget in card.winfo_descendants():
                if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                    self._scale_font(widget)
    
    def _scale_font(self, widget):
        if not hasattr(widget, 'cget'):
            return
            
        try:
            current_font = widget.cget("font")
            if isinstance(current_font, str):
                # If font is stored as a string (family, size)
                family, size = current_font.split()
                new_size = int(float(size) * self.font_scale)
                widget.config(font=(family, new_size))
            elif isinstance(current_font, tuple):
                # If font is stored as a tuple (family, size, style)
                family, size = current_font[0], current_font[1]
                style = current_font[2] if len(current_font) > 2 else ""
                new_size = int(float(size) * self.font_scale)
                widget.config(font=(family, new_size, style))
        except Exception:
            # Skip widgets where font scaling fails
            pass
    
    def toggle_high_contrast(self):
        # Toggle high contrast mode
        self.high_contrast = not self.high_contrast
        
        if self.high_contrast:
            # High contrast mode
            bg_color = "#1a1a1a"  # Dark background
            fg_color = "#ffffff"  # White text
            card_bg = "#333333"   # Dark card background
        else:
            # Normal mode
            bg_color = COLORS["bg_secondary"]
            fg_color = COLORS["text_primary"]
            card_bg = COLORS["card_bg"]
        
        # Apply to main container
        self.config(bg=bg_color)
        
        # Apply to scroll frame and canvas
        self.scroll_frame.config(bg=bg_color)
        self.canvas.config(bg=bg_color)
        self.scenario_container.config(bg=bg_color)
        
        # Apply to all cards/scenarios
        for card_frame in self.scenario_container.winfo_children():
            if isinstance(card_frame, tk.Frame):
                card_frame.config(bg=card_bg)
                
                # Find inner card frame
                for inner_frame in card_frame.winfo_children():
                    if isinstance(inner_frame, tk.Frame):
                        inner_frame.config(bg=card_bg)
                        
                        # Apply to all widgets inside the card
                        for widget in inner_frame.winfo_descendants():
                            if isinstance(widget, tk.Label):
                                widget.config(bg=card_bg, fg=fg_color)
                            elif isinstance(widget, tk.Frame):
                                widget.config(bg=card_bg)
                            elif isinstance(widget, tk.Button):
                                if self.high_contrast:
                                    widget.config(bg="#444444", fg="white")
                                else:
                                    widget.config(**BUTTON_STYLES["primary"])

    def load_scenarios(self):
        try:
            response = requests.get("http://localhost:5000/scenarios", timeout=3)
            response.raise_for_status()
            self.scenarios = response.json()

            for widget in self.scenario_container.winfo_children():
                widget.destroy()

            for s in self.scenarios:
                self._create_card(s)

        except Exception as e:
            error_label = tk.Label(
                self.scenario_container, 
                text=f"Error loading scenarios: {e}", 
                foreground=COLORS["accent_error"],
                bg=COLORS["bg_secondary"],
                font=FONTS["body_small"],
                pady=SPACING["large"]
            )
            error_label.pack(pady=SPACING["large"])

    def _create_card(self, scenario):
        # Create a more modern card with rounded corners effect
        outer_frame = tk.Frame(self.scenario_container, bg=COLORS["card_border"], padx=2, pady=2)
        outer_frame.pack(pady=SPACING["small"], padx=SPACING["large"], fill="x")
        
        card_frame = tk.Frame(
            outer_frame, 
            bg=COLORS["card_bg"], 
            padx=SPACING["medium"], 
            pady=SPACING["medium"]
        )
        card_frame.pack(fill="x")
        
        # Card content
        header_frame = tk.Frame(card_frame, bg=COLORS["card_bg"])
        header_frame.pack(fill="x", anchor="w")
        
        # Small indicator dot showing "available" status
        status = tk.Label(
            header_frame,
            text="●",
            font=FONTS["body_small"],
            fg=COLORS["accent_success"],
            bg=COLORS["card_bg"]
        )
        status.pack(side="left", padx=(0, SPACING["tiny"]))
        
        title = tk.Label(
            header_frame, 
            text=scenario["title"], 
            font=("Helvetica", 14, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_primary"]
        )
        title.pack(side="left")

        desc = tk.Label(
            card_frame, 
            text=scenario["description"], 
            font=FONTS["body_small"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_secondary"],
            justify="left",
            wraplength=500
        )
        desc.pack(anchor="w", pady=(SPACING["small"], SPACING["medium"]))
        
        # Bottom row with button
        btn_frame = tk.Frame(card_frame, bg=COLORS["card_bg"])
        btn_frame.pack(fill="x")
        
        select_btn = tk.Button(
            btn_frame,
            text="Select",
            command=lambda sid=scenario["id"]: self.select_scenario(sid),
            font=FONTS["button_small"],
            **BUTTON_STYLES["primary"]
        )
        select_btn.config(padx=SPACING["medium"], pady=SPACING["tiny"])
        select_btn.pack(side="right")

    def select_scenario(self, scenario_id):
        self.controller.selected_scenario = scenario_id

        # Set full object for audio loop
        for s in self.scenarios:
            if s["id"] == scenario_id:
                self.controller.selected_scenario_obj = s
                break

        print(f"✅ Selected scenario: {scenario_id}")
        self.controller.show_frame("VideoSelectionPage")
