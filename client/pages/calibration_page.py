import tkinter as tk
from tkinter import ttk
from utils.gaze_detection import detect_gaze
import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
from styles import COLORS, FONTS, SPACING, BUTTON_STYLES

class CalibrationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_secondary"])
        self.controller = controller
        self.controller.calibration_data = []
        self.controller.calibration_page = self  # Store reference to this page

        self.predicted_points = []
        self.target_points = []

        # --- UI Elements ---
        self.create_navbar()

        # Main container with proper centering
        self.main_container = tk.Frame(self, bg=COLORS["bg_secondary"])
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Content frame for instructions and buttons
        self.content_frame = tk.Frame(self.main_container, bg=COLORS["bg_secondary"])
        self.content_frame.pack(fill="both", expand=True, padx=SPACING["large"], pady=SPACING["small"])

        # Header/Title
        self.title = tk.Label(
            self.content_frame,
            text="Gaze Calibration",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
        )
        self.title.pack(pady=SPACING["medium"])

        # Instructions
        self.instructions = tk.Label(
            self.content_frame,
            text="Look at the dot on screen when it appears.\nFollow the calibration dots to complete setup.",
            font=FONTS["body"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            justify="center"
        )
        self.instructions.pack(pady=SPACING["medium"])

        # Calibration canvas (centered)
        self.dot_canvas = tk.Canvas(
            self.main_container, 
            width=800, 
            height=480, 
            bg=COLORS["bg_secondary"], 
            highlightthickness=0
        )
        self.dot_canvas.pack(padx=SPACING["large"], pady=SPACING["medium"])

        # Progress indicator (initially hidden)
        self.progress_label = tk.Label(
            self.main_container,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
        )
        
        # Button container for better alignment
        self.button_container = tk.Frame(self.content_frame, bg=COLORS["bg_secondary"])
        self.button_container.pack(pady=SPACING["medium"])
        
        # Start button
        self.start_button = tk.Button(
            self.button_container,
            text="Start Calibration",
            command=self.start_calibration,
            font=FONTS["button"],
            **BUTTON_STYLES["primary"],
            width=20
        )
        self.start_button.pack(pady=SPACING["small"])
        
        # Skip button
        self.skip_button = tk.Button(
            self.button_container,
            text="Skip Calibration",
            command=self.skip_calibration,
            font=FONTS["button"],
            **BUTTON_STYLES["secondary"],
            width=20
        )
        self.skip_button.pack(pady=SPACING["small"])

        # --- Calibration targets ---
        self.calibration_points = [
            (100, 100), (400, 100), (700, 100),
            (100, 240), (400, 240), (700, 240),
            (100, 380), (400, 380), (700, 380),
        ]

        self.current_index = 0
        
        # Accessibility settings
        self.font_scale = 1.0
        self.high_contrast = False

    def create_navbar(self):
        navbar = tk.Frame(self, bg=COLORS["navbar_bg"], height=40)
        navbar.pack(side="top", fill="x")
        
        logo = tk.Label(navbar, text="CareCase", font=FONTS["logo"], bg=COLORS["navbar_bg"], fg=COLORS["text_primary"])
        logo.pack(side="left", padx=SPACING["small"])

        back_btn = tk.Button(navbar, text="← Back", command=lambda: self.controller.show_frame("HomePage"))
        back_btn.pack(side="right", padx=SPACING["small"], pady=SPACING["small"])
        
        # Right-aligned elements
        help_btn = tk.Button(navbar, text="Help", width=8)
        help_btn.pack(side="right", padx=SPACING["small"], pady=SPACING["small"])
        
        # Language dropdown
        lang_var = tk.StringVar(value="English")
        lang_dropdown = ttk.Combobox(navbar, textvariable=lang_var, width=10, state="readonly")
        lang_dropdown['values'] = ('English', 'Spanish', 'French')
        lang_dropdown.pack(side="right", padx=SPACING["small"], pady=SPACING["small"])
        
        # Accessibility button with popup function
        access_btn = tk.Button(navbar, text="♿", width=3, command=self.show_accessibility_options)
        access_btn.pack(side="right", padx=SPACING["small"], pady=SPACING["small"])

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
        self._scale_font(self.title)
        self._scale_font(self.instructions)
        self._scale_font(self.progress_label)
        self._scale_font(self.start_button)
        self._scale_font(self.skip_button)
        
        # Apply to button container and other frames if needed
        for widget in self.winfo_children():
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
            new_button_bg = "#444444"  # Dark button
            new_button_fg = "#ffffff"  # White button text
        else:
            # Normal mode (use default theme colors)
            new_bg = COLORS["bg_secondary"]
            new_fg = COLORS["text_primary"]
            new_button_bg = BUTTON_STYLES["primary"]["bg"]
            new_button_fg = BUTTON_STYLES["primary"]["fg"]
        
        # Apply to main containers
        self.config(bg=new_bg)
        self.main_container.config(bg=new_bg)
        self.content_frame.config(bg=new_bg)
        self.button_container.config(bg=new_bg)
        self.dot_canvas.config(bg=new_bg)
        
        # Apply to labels
        self.title.config(bg=new_bg, fg=new_fg)
        self.instructions.config(bg=new_bg, fg=new_fg)
        self.progress_label.config(bg=new_bg, fg=new_fg)
        
        # Apply to buttons (keep original colors for primary/secondary distinction)
        if not self.high_contrast:
            self.start_button.config(**BUTTON_STYLES["primary"])
            self.skip_button.config(**BUTTON_STYLES["secondary"])
        else:
            # Custom high contrast button styles
            self.start_button.config(bg=new_button_bg, fg=new_button_fg)
            self.skip_button.config(bg="#333333", fg=new_button_fg)

    def start_calibration(self):
        # Open webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Could not open webcam for calibration.")
            return
        
        # --- Warm-up read ---
        for _ in range(5):
            ret, _ = self.cap.read()

       
        # Hide instructions and buttons
        self.content_frame.pack_forget()
        
        # Show progress indicator
        self.progress_label.config(text="Calibrating... (1/9)")
        self.progress_label.pack(pady=SPACING["small"])
        
        # Start calibration process
        self.show_next_dot()

    def skip_calibration(self):
        # If skipped, calibration_data stays empty
        self.controller.calibration_data = None
        self.controller.show_frame("SelectScenarioPage")

    def show_next_dot(self):
        if self.current_index >= len(self.calibration_points):
            self.finish_calibration()
            return
        
        # Update progress indicator
        self.progress_label.config(text=f"Calibrating... ({self.current_index+1}/{len(self.calibration_points)})")
        
        # Clear canvas and show current dot
        self.dot_canvas.delete("all")
        x, y = self.calibration_points[self.current_index]
        
        # Draw larger, more visible dot
        self.dot_canvas.create_oval(x-15, y-15, x+15, y+15, fill=COLORS["accent_primary"], outline=COLORS["accent_hover"], width=2)
        
        # Wait longer for user to look at dot (1.5 seconds) then capture
        self.after(1500, self.capture_gaze_data)

    def capture_gaze_data(self):
        success, frame = self.cap.read()
        if not success or frame is None:
            print("❌ Failed to capture webcam frame.")
            self.current_index += 1
            self.after(500, self.show_next_dot)
            return
        
        # Ensure frame dimensions
        h, w = frame.shape[:2]
        if h == 0 or w == 0:
            print("⚠️ Captured frame is empty.")
            self.current_index += 1
            self.after(500, self.show_next_dot)
            return


        gaze = detect_gaze(frame)

        landmarks = gaze.get("landmarks", {})
        left_iris = landmarks.get("left_iris", [])
        right_iris = landmarks.get("right_iris", [])

        if left_iris and right_iris:
            # Get centers
            lx, ly = np.mean(left_iris, axis=0)
            rx, ry = np.mean(right_iris, axis=0)

            raw_x = (lx + rx) / 2
            raw_y = (ly + ry) / 2

            # Save real gaze point
            self.predicted_points.append((raw_x, raw_y))
            self.target_points.append(self.calibration_points[self.current_index])
        else:
            print("⚠️ No gaze detected, skipping point.")


        self.current_index += 1
        self.after(500, self.show_next_dot)


    def finish_calibration(self):
        predicted = np.array(self.predicted_points)
        target = np.array(self.target_points)

        # --- Bias Correction ---
        bias = np.mean(target - predicted, axis=0)

        # --- Optional Linear Regression ---
        model = LinearRegression().fit(predicted, target)

        # Save calibration globally
        self.controller.calibration_data = {
            "bias": bias.tolist(),
            "regression_coef": model.coef_.tolist(),
            "regression_intercept": model.intercept_.tolist()
        }

        # Hide progress label
        self.progress_label.pack_forget()
        
        # Clear canvas
        self.dot_canvas.delete("all")
        
        # Show completion message
        completion_frame = tk.Frame(self.main_container, bg=COLORS["bg_secondary"])
        completion_frame.pack(fill="both", expand=True, padx=SPACING["large"], pady=SPACING["large"])
        
        tk.Label(
            completion_frame,
            text="Calibration Complete!",
            font=FONTS["subtitle"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["accent_success"],
        ).pack(pady=SPACING["small"])
        
        tk.Label(
            completion_frame,
            text="Your session is now personalized.",
            font=FONTS["body"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
        ).pack(pady=SPACING["small"])

        # Continue button
        continue_btn = tk.Button(
            completion_frame,
            text="Continue",
            command=lambda: self.controller.show_frame("SelectScenarioPage"),
            font=FONTS["button"],
            **BUTTON_STYLES["primary"],
            width=20
        )
        continue_btn.pack(pady=SPACING["large"])

        # Release webcam
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()


    def adjust_gaze(self, x, y):
        # Usage: pass new gaze detection here to adjust it
        calibration = getattr(self.controller, "calibration_data", None)
        if calibration:
            bias = np.array(self.controller.calibration_data["bias"])
            coef = np.array(self.controller.calibration_data["regression_coef"])
            intercept = np.array(self.controller.calibration_data["regression_intercept"])

            corrected = np.dot(np.array([x, y]), coef) + intercept
            return corrected[0], corrected[1]
        else:
            return x, y  # No calibration done yet
