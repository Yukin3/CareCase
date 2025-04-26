import tkinter as tk
from tkinter import ttk
import random
import requests
import time

COLORS = {
    "bg_secondary": "#f0f4f8",
    "text_primary": "#2D3748",
    "navbar_bg": "#abd4f5",
}
FONTS = {
    "logo": ("Helvetica", 14, "bold"),
    "body": ("Helvetica", 12),
    "subtitle": ("Helvetica", 18, "bold"),
}

SPACING = {
    "tiny": 4,
    "small": 10,
    "medium": 15,
}

BUTTON_STYLES = {
    "primary": {"bg": "#3182CE", "fg": "white", "borderwidth": 0},
    "secondary": {"bg": "#E2E8F0", "fg": "#1A202C", "borderwidth": 0}
}

class DiagnosisTrainerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.score = 0
        self.rounds_played = 0
        self.total_rounds = 5
        self.history = []
        
        # Accessibility settings
        self.font_scale = 1.0
        self.high_contrast = False

        self.setup_ui()

    def setup_ui(self):
        self.create_navbar()

        self.title = tk.Label(self, text="Diagnosis Trainer", font=("Helvetica", 18, "bold"), bg="white")
        self.title.pack(pady=10)

        self.case_text = tk.Label(self, text="Press 'Generate Case' to start!", font=("Helvetica", 12), bg="white", wraplength=500, justify="left")
        self.case_text.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="white")
        self.button_frame.pack(pady=5)

        self.generate_btn = ttk.Button(self.button_frame, text="Generate Case", command=self.generate_case)
        self.generate_btn.pack(side="left", padx=10)

        self.yes_btn = ttk.Button(self.button_frame, text="✅ Positive", command=lambda: self.submit_guess("positive"))
        self.no_btn = ttk.Button(self.button_frame, text="❌ Negative", command=lambda: self.submit_guess("negative"))

        self.status_label = tk.Label(self, text="", font=("Helvetica", 10), bg="white")
        self.status_label.pack(pady=5)

        self.back_btn = ttk.Button(self, text="← Back to Home", command=lambda: self.controller.show_frame("HomePage"))
        self.back_btn.pack(pady=20)

    def create_navbar(self):
        navbar = tk.Frame(self, bg=COLORS["navbar_bg"], height=40)
        navbar.pack(side="top", fill="x")

        logo = tk.Label(navbar, text="CareCase", font=FONTS["logo"], bg=COLORS["navbar_bg"], fg=COLORS["text_primary"])
        logo.pack(side="left", padx=10)

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
        
        bg_color = "#1a1a1a" if self.high_contrast else "white"
        fg_color = "white" if self.high_contrast else COLORS["text_primary"]
        
        # Apply to main container
        self.config(bg=bg_color)
        
        # Apply to all direct widgets
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
                # Update frame children
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=bg_color, fg=fg_color)
        
        # Apply to button frame
        self.button_frame.config(bg=bg_color)
        
        # Apply to status label
        self.status_label.config(bg=bg_color, fg=fg_color)

    def generate_case(self):
        try:
            diseases = requests.get("http://localhost:5000/diseases").json()
            selected = random.choice(diseases)

            case = requests.get(f"http://localhost:5000/disease/profile?disease={selected}").json()
            self.current_case = case

            profile = case["patient_profile"]
            symptoms = case["symptoms"]

            symptom_text = "\n".join(
                [f"- {symptom.replace('_', ' ').capitalize()}: {'✅' if value else '❌'}" for symptom, value in symptoms.items()]
            )

            profile_text = f"Age: {profile['age']}\nGender: {profile['gender'].capitalize()}\nBlood Pressure: {profile['blood_pressure'].capitalize()}\nCholesterol: {profile['cholesterol_level'].capitalize()}"

            full_text = f"{profile_text}\n\nSymptoms:\n{symptom_text}\n\nDoes this patient have {case['disease']}?"
            self.case_text.config(text=full_text)

            self.yes_btn.pack(side="left", padx=10)
            self.no_btn.pack(side="left", padx=10)

            self.status_label.config(text="")

        except Exception as e:
            self.case_text.config(text=f"❌ Error fetching case: {e}")

    def submit_guess(self, guess):
        if not hasattr(self, "current_case"):
            self.status_label.config(text="⚠️ No case generated yet!")
            return

        actual = self.current_case["outcome"]

        correct = guess == actual
        if correct:
            self.score += 1

        self.history.append({
            "disease": self.current_case["disease"],
            "user_guess": guess,
            "actual_outcome": actual,
            "correct": correct,
            "timestamp": time.time()
        })

        self.rounds_played += 1

        if self.rounds_played >= self.total_rounds:
            self.finish_quiz()
        else:
            self.status_label.config(text=f"✅ Guess saved! {self.rounds_played}/{self.total_rounds} rounds completed.")
            self.after(800, self.generate_case)  # 🌀 Wait 800ms, then auto-generate next case

    def finish_quiz(self):
        result_text = f"🏁 Quiz Completed!\n\nFinal Score: {self.score}/{self.total_rounds}\n\n"
        for i, entry in enumerate(self.history, 1):
            status = "✅ Correct" if entry["correct"] else "❌ Incorrect"
            result_text += f"{i}. {entry['disease']}: {status}\n"

        self.case_text.config(text=result_text)
        self.yes_btn.pack_forget()
        self.no_btn.pack_forget()
        self.generate_btn.config(text="🔄 Restart Quiz", command=self.restart_quiz)
        self.status_label.config(text="")

    def restart_quiz(self):
        self.score = 0
        self.rounds_played = 0
        self.history = []
        self.status_label.config(text="")
        self.case_text.config(text="Press 'Generate Case' to start!")
        self.generate_btn.config(text="🔄 Generate Case", command=self.generate_case)
