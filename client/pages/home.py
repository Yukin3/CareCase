import tkinter as tk
from tkinter import ttk
from styles import COLORS, FONTS, SPACING, BUTTON_STYLES

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_primary"])
        self.controller = controller
        self.content = None  # We'll use this for animation
        
        # Accessibility settings
        self.font_scale = 1.0
        self.high_contrast = False
        
        # Create a navbar frame
        self.create_navbar()
        
        # Create main content
        self.create_content()

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
        logo.pack(side="left", padx=10)
        
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
                
        # Apply to content widgets
        if self.content:
            for widget in self.content.winfo_descendants():
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
            # High contrast mode (dark background, light text)
            new_bg = "#1a1a1a"  # Dark background
            new_fg = "#ffffff"  # White text
            new_btn_bg = "#444444"  # Dark button
            new_btn_fg = "#ffffff"  # White button text
        else:
            # Normal mode (use default theme colors)
            new_bg = COLORS["bg_primary"]
            new_fg = COLORS["text_primary"]
            new_btn_bg = BUTTON_STYLES["primary"]["bg"]
            new_btn_fg = BUTTON_STYLES["primary"]["fg"]
        
        # Apply to main container
        self.config(bg=new_bg)
        
        # Apply to content frame
        if self.content:
            self.content.config(bg=new_bg)
            
            # Apply to all child widgets
            for widget in self.content.winfo_descendants():
                if isinstance(widget, tk.Label):
                    widget.config(bg=new_bg, fg=new_fg)
                elif isinstance(widget, tk.Button):
                    widget.config(bg=new_btn_bg, fg=new_btn_fg)
                elif isinstance(widget, tk.Frame):
                    widget.config(bg=new_bg)

    def create_content(self):
        self.content = tk.Frame(self, bg=COLORS["bg_primary"], padx=SPACING["xlarge"], pady=SPACING["xlarge"])
        self.content.place(relx=0.5, rely=0.5, anchor="center")

        # Logo/Icon
        logo_frame = tk.Frame(self.content, bg=COLORS["bg_primary"])
        logo_frame.pack(pady=(0, SPACING["large"]))
        
        logo_icon = tk.Label(
            logo_frame,
            text="👩🏾‍⚕️",
            font=("Helvetica", 40),
            bg=COLORS["bg_primary"]
        )
        logo_icon.pack()

        # Title with better styling
        title = tk.Label(
            self.content,
            text="CareCase",
            font=FONTS["title"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"]
        )
        title.pack(pady=(0, SPACING["medium"]))

        desc = tk.Label(
            self.content,
            text="A culturally diverse AI-powered simulation platform for clinical training.",
            font=FONTS["body"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_secondary"],
            wraplength=500,
            justify="center"
        )
        desc.pack(pady=(0, SPACING["xlarge"]))

        # Simulations button
        start_btn = tk.Button(
            self.content,
            text="Interaction Simulator",
            command=lambda: self.controller.show_frame("CalibrationPage"),
            font=FONTS["button"],
            bg=BUTTON_STYLES["primary"]["bg"],
            fg=BUTTON_STYLES["primary"]["fg"],
            padx=SPACING["large"],
            pady=SPACING["small"],
            relief=BUTTON_STYLES["primary"]["relief"],
            activebackground=BUTTON_STYLES["primary"]["activebackground"],
            activeforeground=BUTTON_STYLES["primary"]["activeforeground"],
            cursor=BUTTON_STYLES["primary"]["cursor"]
        )
        start_btn.pack()

        # Trainer button 
        start_btn = tk.Button(
            self.content,
            text="Diagnosis Trainer",
            command=lambda: self.controller.show_frame("DiagnosisTrainerPage"),
            font=FONTS["button"],
            bg=BUTTON_STYLES["primary"]["bg"],
            fg=BUTTON_STYLES["primary"]["fg"],
            padx=SPACING["large"],
            pady=SPACING["small"],
            relief=BUTTON_STYLES["primary"]["relief"],
            activebackground=BUTTON_STYLES["primary"]["activebackground"],
            activeforeground=BUTTON_STYLES["primary"]["activeforeground"],
            cursor=BUTTON_STYLES["primary"]["cursor"]
        )
        start_btn.pack()

                # Appendix button 
        start_btn = tk.Button(
            self.content,
            text="Medicine Appendix",
            command=lambda: self.controller.show_frame("MedicinesPage"),
            font=FONTS["button"],
            bg=BUTTON_STYLES["primary"]["bg"],
            fg=BUTTON_STYLES["primary"]["fg"],
            padx=SPACING["large"],
            pady=SPACING["small"],
            relief=BUTTON_STYLES["primary"]["relief"],
            activebackground=BUTTON_STYLES["primary"]["activebackground"],
            activeforeground=BUTTON_STYLES["primary"]["activeforeground"],
            cursor=BUTTON_STYLES["primary"]["cursor"]
        )
        start_btn.pack()

        self.content.update_idletasks()

    def on_show(self):
        self.animate_in()

    def animate_in(self):
        # Enhanced fade-in animation
        def step(y_offset, opacity=0.0):
            if opacity >= 1.0:
                self.content.place_configure(rely=0.5)
                return
                
            opacity += 0.05
            y_offset -= 0.005
            
            self.content.place_configure(rely=0.5 - y_offset)
            self.after(16, lambda: step(y_offset, opacity))

        step(0.1)  # Start slightly off-center and animate up
