import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Dummy style dictionaries
COLORS = {
    "bg_secondary": "#f0f4f8",
    "card_bg": "#ffffff",
    "card_border": "#dbefff",
    "text_primary": "#2D3748",
    "text_secondary": "#4A5568",
    "accent_error": "#e53e3e",
    "navbar_bg": "#abd4f5"
}
FONTS = {
    "logo": ("Helvetica", 14, "bold"),
    "subtitle": ("Helvetica", 16, "bold"),
    "body_small": ("Helvetica", 10),
    "body": ("Helvetica", 12),
    "button_small": ("Helvetica", 10, "bold")
}
SPACING = {
    "tiny": 4,
    "small": 8,
    "medium": 16,
    "large": 24
}
BUTTON_STYLES = {
    "primary": {"bg": "#3182CE", "fg": "white", "borderwidth": 0},
    "secondary": {"bg": "#E2E8F0", "fg": "#1A202C", "borderwidth": 0}
}

class MedicinesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_secondary"])
        self.controller = controller
        self.medicines = []

        # Accessibility settings
        self.font_scale = 1.0
        self.high_contrast = False

        self.create_navbar()

        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"])
        content_frame.pack(fill="both", expand=True, padx=SPACING["large"], pady=SPACING["small"])

        header = tk.Label(
            content_frame,
            text="Medicines",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        
        # --- Search Bar ---
        search_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        search_frame.pack(fill="x", pady=(0, SPACING["medium"]))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=(0, SPACING["small"]))
       
        search_entry.bind("<KeyRelease>", lambda event: self.search_medicines())  # Live search

        search_btn = ttk.Button(search_frame, text="Search", command=self.search_medicines)
        search_btn.pack(side="left")
        
        header.pack(anchor="w", pady=(0, SPACING["medium"]))

        self.scroll_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        self.scroll_frame.pack(fill="both", expand=True)

        # --- Back Button ---
        back_btn = tk.Button(
            content_frame,
            text="← Back to Home",
            font=FONTS["button_small"],
            command=lambda: self.controller.show_frame("HomePage"),
            **BUTTON_STYLES["secondary"]
        )
        back_btn.pack(anchor="w", pady=(0, SPACING["small"]))


        self.canvas = tk.Canvas(self.scroll_frame, bg=COLORS["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)

        self.card_container = tk.Frame(self.canvas, bg=COLORS["bg_secondary"])
        self.card_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.card_container.grid_columnconfigure(0, weight=1)
        self.card_container.grid_columnconfigure(1, weight=1)

        self.canvas.create_window((0, 0), window=self.card_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_medicines()
        self.bind_mousewheel(self.canvas)


    def create_navbar(self):
        navbar = tk.Frame(self, bg=COLORS["navbar_bg"], height=40)
        navbar.pack(side="top", fill="x")

        logo = tk.Label(navbar, text="CareCase", font=FONTS["logo"], bg=COLORS["navbar_bg"], fg=COLORS["text_primary"])
        logo.pack(side="left", padx=SPACING["small"])

        help_btn = ttk.Button(navbar, text="Help", width=8)
        help_btn.pack(side="right", padx=SPACING["tiny"], pady=SPACING["tiny"])

        lang_var = tk.StringVar(value="English")
        lang_dropdown = ttk.Combobox(navbar, textvariable=lang_var, width=10, state="readonly")
        lang_dropdown['values'] = ('English', 'Spanish', 'French')
        lang_dropdown.pack(side="right", padx=SPACING["tiny"], pady=SPACING["tiny"])

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
                
        # Apply to card container and its children
        for card in self.card_container.winfo_children():
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
        self.card_container.config(bg=bg_color)
        
        # Apply to all cards
        for card_frame in self.card_container.winfo_children():
            if isinstance(card_frame, tk.Frame):
                card_frame.config(bg=card_bg)
                
                # Apply to all widgets inside each card
                for widget in card_frame.winfo_descendants():
                    if isinstance(widget, tk.Label):
                        widget.config(bg=card_bg, fg=fg_color)
                    elif isinstance(widget, tk.Frame):
                        widget.config(bg=card_bg)
                    elif isinstance(widget, tk.Button):
                        if self.high_contrast:
                            widget.config(bg="#444444", fg="white")
                        else:
                            widget.config(**BUTTON_STYLES["primary"])

    def load_medicines(self):
        try:
            response = requests.get("http://localhost:5000/medicines?limit=30")
            response.raise_for_status()
            self.medicines = response.json()

            for widget in self.card_container.winfo_children():
                widget.destroy()

            for index, med in enumerate(self.medicines):
                row = index // 2
                col = index % 2
                self.create_card(med, row, col)

        except Exception as e:
            tk.Label(self.card_container, text=f"Error loading medicines: {e}", bg=COLORS["bg_secondary"], fg=COLORS["accent_error"]).pack()

    def create_card(self, med, row, col):
        outer = tk.Frame(self.card_container, bg=COLORS["card_border"], padx=2, pady=2)
        outer.grid(row=row, column=col, padx=SPACING["medium"], pady=SPACING["small"], sticky="nsew")

        card = tk.Frame(outer, bg=COLORS["card_bg"], padx=SPACING["medium"], pady=SPACING["medium"])
        card.pack(fill="both", expand=True)

        tk.Label(card, text=med["name"], font=("Helvetica", 14, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_primary"]).pack(anchor="w")
        tk.Label(card, text=f"{med['strength']} - {med['dosage_form']}", font=FONTS["body_small"], bg=COLORS["card_bg"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(4, 4))
        tk.Label(card, text=f"Classification: {med['classification']}", font=FONTS["body_small"], bg=COLORS["card_bg"], fg=COLORS["text_secondary"]).pack(anchor="w")

        view_btn = tk.Button(card, text="View", font=FONTS["button_small"], **BUTTON_STYLES["primary"],
                             command=lambda: self.show_modal(med))
        view_btn.pack(anchor="e", pady=(8, 0))

    def show_modal(self, med):
        modal = tk.Toplevel(self)
        modal.title("Medicine Info")
        modal.transient(self)
        modal.grab_set()
        modal.configure(bg="white")

        content = tk.Frame(modal, bg="white", padx=20, pady=20)
        content.pack()

        for key in ["name", "strength", "dosage_form", "classification", "category", "manufacturer", "indication"]:
            tk.Label(content, text=f"{key.capitalize().replace('_', ' ')}:", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
            tk.Label(content, text=med.get(key, "N/A"), font=FONTS["body_small"], bg="white").pack(anchor="w", pady=(0, 10))

        ttk.Button(content, text="Close", command=modal.destroy).pack(pady=(10, 0))
    
    def bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda e: widget.bind_all("<MouseWheel>", self._on_mousewheel))
        widget.bind("<Leave>", lambda e: widget.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def search_medicines(self):
        query = self.search_var.get().strip().lower()

        if not query:
            self.load_medicines()
            return

        # Basic frontend filtering — optional: replace with backend query param later
        filtered = [
            med for med in self.medicines
            if query in med["name"].lower()
            or query in med["strength"].lower()
            or query in med["dosage_form"].lower()
            or query in med["classification"].lower()
            or query in med["category"].lower()
            or query in med["manufacturer"].lower()
            or query in med["indication"].lower()
        ]

        for widget in self.card_container.winfo_children():
            widget.destroy()

        for index, med in enumerate(filtered):
            row = index // 2
            col = index % 2
            self.create_card(med, row, col)
