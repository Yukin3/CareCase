import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import requests  # For real API call

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f4f8")
        self.controller = controller

        self.title_label = ttk.Label(self, text="Fetching Results...", font=("Helvetica", 20, "bold"), foreground="#2D3748", background="#f0f4f8")
        self.title_label.pack(pady=(40, 20))
        # Score bar
        self.score_bar = ttk.Progressbar(
            self,
            length=300,
            mode="determinate",
            maximum=10  # Our scale is out of 10
        )
        self.score_bar.pack(pady=(0, 20))

        # --- Create scrollable area ---
        self.canvas = tk.Canvas(self, bg="#f0f4f8", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#f0f4f8")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


        self.retry_button = ttk.Button(self, text="Restart Simulation", command=lambda: controller.show_frame("SimulationScreenPage"))
        self.home_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        self.retry_button.pack(in_=self.scroll_frame, pady=10)
        self.home_button.pack(in_=self.scroll_frame, pady=5)


        # 🖱️ Bind mouse scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


    def on_show(self):
        self.title_label.config(text="Fetching Results...")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        threading.Thread(target=self.load_results, daemon=True).start()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def load_results(self):
        time.sleep(1)  # Simulate delay

        log = getattr(self.controller.last_logger, "get_log", lambda: None)()
        if not log:
            self.title_label.config(text="❌ No session log found.")
            return

        try:
            response = requests.post("http://localhost:5000/score?online=true", json=log)
            raw_result = response.json()
            print("🔍 Final parsed result:", raw_result)


            # Pull out fields safely
            overall_score = raw_result.get("score", 0.0)
            interaction = raw_result.get("interaction", {})
            gaze = raw_result.get("gaze", {})

            # Update title with overall score
            self.title_label.config(text=f"📝Final Score: {round(overall_score, 2)}/10")
            self.score_bar["value"] = overall_score  # Set the progress bar



            # Show feedback cards
            self.result_card("💬 Feedback", interaction.get("feedback", "No feedback available."))
            for turn in interaction.get("per_turn_feedback", []):
                self.result_card(
                    f"Turn {turn.get('turn', '?')}",
                    f"{turn.get('student_reply', 'N/A')}\nScore: {turn.get('score', '?')}/3\n💡 {turn.get('comment', '')}"
                )

            # Show gaze feedback
            self.result_card("👁️ Gaze Feedback", gaze.get("feedback", "No gaze data available."))

        
        except Exception as e:
            print("❌ Error loading results:", e)
            self.title_label.config(text="❌ Failed to fetch results.")
            #! BAILOUT DEMO FALLBACK
            # result = {
            #     "score": 7.8,
            #     "feedback": "Great job maintaining clarity. Could improve on empathy.",
            #     "per_turn_feedback": [
            #         {"turn": 1, "student_reply": "What did you eat?", "score": 2.5, "comment": "Good direction, could be more empathetic."},
            #         {"turn": 2, "student_reply": "Did you drink water?", "score": 3, "comment": "Clear and helpful."}
            #     ]
            # }

    def result_card(self, title, text):
        frame = tk.Frame(self.scroll_frame, bg="#FFFFFF", bd=1, relief="solid")
        frame.pack(padx=30, pady=10, fill="x")

        title_label = tk.Label(frame, text=title, bg="white", font=("Helvetica", 12, "bold"), anchor="w")
        title_label.pack(anchor="w", padx=10, pady=(10, 0))

        content_label = tk.Label(frame, text=text, bg="white", font=("Helvetica", 11), justify="left", anchor="w", wraplength=480)
        content_label.pack(padx=10, pady=(0, 10), anchor="w")
