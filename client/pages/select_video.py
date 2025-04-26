import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import io
import requests
from styles import COLORS, FONTS, SPACING, BUTTON_STYLES

class VideoSelectionPage(tk.Frame):
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
            text="Select a Video", 
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        header.pack(side="left")
        
        # Small icon next to header
        icon = tk.Label(
            header_frame,
            text="🎥",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        icon.pack(side="left", padx=(SPACING["small"], 0))

        # Scrollable video container
        self.scroll_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.scroll_frame, bg=COLORS["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        
        self.video_frame = tk.Frame(self.canvas, bg=COLORS["bg_secondary"])
        self.video_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.video_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Status label with improved styling
        self.status_label = tk.Label(
            content_frame, 
            text="Fetching videos...", 
            font=FONTS["body_small"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.status_label.pack(pady=SPACING["small"])

        # Footer with back button
        footer = tk.Frame(content_frame, bg=COLORS["bg_secondary"], height=50)
        footer.pack(fill="x", pady=(SPACING["small"], SPACING["tiny"]))
        
        back_btn = tk.Button(
            footer, 
            text="← Back", 
            command=lambda: controller.show_frame("SelectScenarioPage"),
            font=FONTS["body_small"],
            **BUTTON_STYLES["secondary"]
        )
        back_btn.config(padx=SPACING["medium"], pady=SPACING["tiny"])
        back_btn.pack(side="left", pady=SPACING["small"])

        # Compute images directory relative to the client script location
        self.backend_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "server", "images"))

    def create_navbar(self):
        navbar = tk.Frame(self, bg=COLORS["navbar_bg"], height=40)
        navbar.pack(side="top", fill="x")
        
        # Logo/home button
        logo = tk.Label(
            navbar, 
            text="CareCase", 
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
                
        # Apply to video frame and its children
        for card in self.video_frame.winfo_children():
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
        
        # Apply to all main frames
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
        
        # Apply to scroll frame and canvas
        self.scroll_frame.config(bg=bg_color)
        self.canvas.config(bg=bg_color)
        self.video_frame.config(bg=bg_color)
        
        # Apply to all video cards
        for card_frame in self.video_frame.winfo_children():
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
        
        # Apply to status label                
        self.status_label.config(bg=bg_color, fg=fg_color)

    def populate_videos(self):
        scenario_id = self.controller.selected_scenario
        try:
            response = requests.get(f"http://127.0.0.1:5000/videos?scenario={scenario_id}", timeout=3)
            videos = response.json()

            print(f"✅ Fetched {len(videos)} videos for scenario_id={scenario_id}")

            for widget in self.video_frame.winfo_children():
                widget.destroy()

            if not videos:
                self.status_label.config(text="No videos found for this scenario.")
                return

            self.status_label.config(text=f"{len(videos)} video(s) available:")

            for video in videos:
                self._create_video_card(video)

        except Exception as e:
            print(f"❌ Error fetching videos: {e}")
            self.status_label.config(text=f"⚠️ Error fetching videos: {e}")

    def _create_video_card(self, video):
        # Create a more modern card with rounded corners effect
        outer_frame = tk.Frame(self.video_frame, bg=COLORS["card_border"], padx=2, pady=2)
        outer_frame.pack(pady=SPACING["small"], padx=SPACING["large"], fill="x")
        
        card = tk.Frame(
            outer_frame, 
            bg=COLORS["card_bg"], 
            padx=SPACING["medium"], 
            pady=SPACING["medium"]
        )
        card.pack(fill="x")

        # Image container with better styling
        img_container = tk.Frame(card, bg=COLORS["card_bg"], width=130, height=100)
        img_container.pack(side="left", padx=SPACING["small"], pady=SPACING["small"])
        img_container.pack_propagate(False)  # Maintain fixed size
        
        # Load image
        img_label = tk.Label(img_container, bg=COLORS["card_bg"])
        img_label.pack(fill="both", expand=True)

        try:
            print("Attempting to load thumbnail:", video["thumbnail_url"])
            if video["thumbnail_url"].startswith("http"):
                response = requests.get(video["thumbnail_url"], timeout=5)
                print("Remote thumbnail status code:", response.status_code)
                response.raise_for_status()
                img_data = Image.open(io.BytesIO(response.content))
            else:
                image_path = os.path.join(self.backend_images_dir, os.path.basename(video["thumbnail_url"]))
                print("📁 Local absolute path:", image_path)
                img_data = Image.open(image_path)   # Local path

            img_data = img_data.resize((120, 90))
            photo = ImageTk.PhotoImage(img_data)
            img_label.config(image=photo)
            img_label.image = photo
        except Exception as e:
            print("⚠️ Thumbnail failed:", e)
            img_label.config(text="❌ No preview", fg=COLORS["accent_error"])

        # Content container
        content_frame = tk.Frame(card, bg=COLORS["card_bg"])
        content_frame.pack(side="left", fill="both", expand=True, padx=SPACING["medium"])
        
        # Title with better styling
        title = tk.Label(
            content_frame, 
            text=video["title"], 
            font=("Helvetica", 14, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_primary"],
            anchor="w",
            justify="left"
        )
        title.pack(fill="x", anchor="w", pady=(SPACING["tiny"], SPACING["tiny"]))
        
        # Description with better styling
        desc = tk.Label(
            content_frame, 
            text=video["description"], 
            font=FONTS["body_small"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_secondary"],
            justify="left",
            anchor="w",
            wraplength=400
        )
        desc.pack(fill="x", anchor="w", pady=(0, SPACING["small"]))
        
        # Button container frame
        btn_frame = tk.Frame(card, bg=COLORS["card_bg"])
        btn_frame.pack(side="right", padx=SPACING["small"], pady=SPACING["small"])
        
        # Select button with better styling
        select_btn = tk.Button(
            btn_frame,
            text="Select Video",
            command=lambda vid=video: self.select_video(vid),
            font=FONTS["button_small"],
            **BUTTON_STYLES["primary"]
        )
        select_btn.config(padx=SPACING["medium"], pady=SPACING["tiny"])
        select_btn.pack()

    def select_video(self, video):
        self.controller.selected_video = video
        print(f"🎬 Selected video: {video['id']}")
        self.controller.show_frame("SimulationScreenPage")

    def on_show(self):
        self.populate_videos()