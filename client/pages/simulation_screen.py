import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk

import os
import cv2
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "server")))
import threading
import time

from utils.audio_loop import run_audio_interaction_line
from utils.interaction_logger import InteractionLogger
from vision.webcam_overlay import init_webcam, get_webcam_frame, release_webcam
from utils.gaze_detection import detect_gaze
from vision.eye_tracking import GazeLogger

class SimulationScreenPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.cap = None
        self.playing = False

        layout = tk.Frame(self, bg="white")
        layout.pack(fill="both", expand=True)

        # LEFT — Video Area (expandable)
        self.video_area = tk.Label(layout, bg="#e0e0e0")
        self.video_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # RIGHT — Sidebar
        self.sidebar = tk.Frame(layout, bg="#f5f5f5", width=250)
        self.sidebar.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        layout.grid_columnconfigure(0, weight=3)
        layout.grid_columnconfigure(1, weight=1)
        layout.grid_rowconfigure(0, weight=1)

        self.webcam_box = tk.Label(self.sidebar, bg="#d0d0d0", width=240, height=180)
        self.webcam_box.pack(pady=(10, 10), padx=10, fill="x")

        self.caption_title = tk.Label(
            self.sidebar,
            text="Caption:\nSpeaker says:",
            bg="white",
            font=("Helvetica", 10, "bold"),
            anchor="w"
        )
        self.caption_title.pack(fill="x", padx=10)

        self.caption_box = tk.Label(
            self.sidebar,
            text="...",
            bg="white",
            wraplength=200,
            justify="left",
            anchor="nw",
            height=6
        )
        self.caption_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Button(self.sidebar, text="← End Simulation", command=self.stop_and_end).pack(pady=10, padx=10, fill="x")

    def on_show(self):
        try:
            # FULL RESET
            self.video_loop_count = 0
            self.playing = False
            if self.cap:
                self.cap.release()
                self.cap = None
            release_webcam()

            # RESTART FRESH
            self.video_loop_count = 0
            self.playing = True

            selected_video = self.controller.selected_video
            local_path = selected_video.get("local_path")

            # Build full path
            abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "server", local_path))
            print(f"▶️ Playing video: {selected_video['title']}")
            print(f"📁 Local path: {abs_path}")

            if not os.path.exists(abs_path):
                print("❌ Video not found at path:", abs_path)
                self.caption_box.config(text="❌ Video file missing.")
                return

            self.cap = cv2.VideoCapture(abs_path)
            self.show_frame()

            if not init_webcam():
                self.caption_box.config(text="❌ Webcam not available.")
            else:
                self.show_webcam_frame()

            self.start_audio_loop()
        
        except Exception as e:
            print("❌ Error in on_show:", e)


    def start_audio_loop(self):
        def loop():
            scenario = self.controller.selected_scenario_obj
            role = "patient"  # or fetch dynamically
            lang = "en-NG"    # or fetch from scenario["language"]
            online = True     # or False if simulating offline fallback

            logger = InteractionLogger(scenario_id=scenario["id"], role=role)
            self.gaze_logger = GazeLogger(
                session_id=logger.session_id,
                logs_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "server", "data", "gaze_logs"))
            )
            turns = 0
            max_turns = 3  # stop after 3 turns for now
            
            while self.playing and turns < max_turns:
                try:
                    transcript = run_audio_interaction_line(
                        scenario=scenario,
                        role=role,
                        language=lang,
                        update_caption_callback=self.render_caption_typewriter,
                        online=online,
                        logger=logger
                    )       
                    turns += 1
                    print("📝 User said:", transcript)
                    time.sleep(1.5)  # Wait before next prompt
                except Exception as e:
                    print("❌ Audio loop error:", e)
                    break

            log_path = logger.save_to_file()
            gaze_path = self.gaze_logger.save_to_file()
            self.controller.last_gaze_logger = self.gaze_logger
            print(f"[<o>] Gaze log saved to {gaze_path}")
            self.controller.last_logger = logger
            print(f"[..] Interaction log saved to {log_path}")
            self.controller.show_frame("ResultsPage")

        threading.Thread(target=loop, daemon=True).start()

    def render_caption_typewriter(self, full_text, delay=30):
        def type_line(i=0):
            if i==0:
                self.caption_box.config(text="")  # clear before starting
            if i <= len(full_text):
                self.caption_box.config(text=full_text[:i])
                self.after(delay, lambda: type_line(i + 1))
        type_line()


    def show_frame(self):
        if not self.playing or not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            # End of video — loop if still playing
            if self.playing:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.after(10, self.show_frame)
            else:
                self.cap.release()
                self.cap = None
            return

        frame = cv2.resize(frame, (480, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_area.imgtk = imgtk
        self.video_area.config(image=imgtk)
        self.after(33, self.show_frame)  # ~30 fps

    def show_webcam_frame(self):
        frame = get_webcam_frame()
        if frame is None:
            self.after(33, self.show_webcam_frame)
            return
        
        # 👁️ Log gaze data
        gaze = detect_gaze(frame)
        if hasattr(self, "gaze_logger") and self.gaze_logger:
            # Get iris centers
            left_iris = gaze.get("landmarks", {}).get("left_iris", [])
            right_iris = gaze.get("landmarks", {}).get("right_iris", [])

            if left_iris and right_iris:
                # Compute center of both irises
                lx, ly = np.mean(left_iris, axis=0)
                rx, ry = np.mean(right_iris, axis=0)

                # Average the two eyes
                raw_gaze_x = (lx + rx) / 2
                raw_gaze_y = (ly + ry) / 2


                # --- Apply calibration adjustment ---
                if hasattr(self.controller, "calibration_page"):
                    adjusted_x, adjusted_y = self.controller.calibration_page.adjust_gaze(raw_gaze_x, raw_gaze_y)
                else:
                    adjusted_x, adjusted_y = raw_gaze_x, raw_gaze_y

                # Now you have adjusted gaze points! Save them
                self.gaze_logger.log_sample(
                    eye_contact=gaze.get("eye_contact", False),
                    gaze_direction=gaze.get("gaze_direction", "unknown"),
                    left_iris=(adjusted_x, adjusted_y),
                    right_iris=(adjusted_x, adjusted_y)  # Optional: or keep separate
                )
            else:
                self.gaze_logger.log_sample(
                    eye_contact=gaze.get("eye_contact", False),
                    gaze_direction=gaze.get("gaze_direction", "unknown")
                )

        frame = cv2.resize(frame, (240, 180))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.webcam_box.config(
            width=240,
            height=180,
            image=imgtk,
            highlightthickness=1,
            highlightbackground="black"
        )
        self.webcam_box.imgtk = imgtk
        self.after(33, self.show_webcam_frame)



    def stop_and_end(self):
        self.playing = False
        if self.cap:
            self.cap.release()
            self.cap = None
        release_webcam()
        self.controller.show_frame("ResultsPage")
