import tkinter as tk
from pages.home import HomePage
from pages.select_scenario import SelectScenarioPage
from pages.simulation_screen import SimulationScreenPage
from pages.results_page import ResultsPage
from pages.select_video import VideoSelectionPage
from pages.medicines_page import MedicinesPage
from pages.diagnosis_trainer_page import DiagnosisTrainerPage
from pages.calibration_page import CalibrationPage


class CareCaseApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CareCase Simulator")
        self.geometry("700x500")
        self.configure(bg="white")

        # Container for all pages
        self.selected_scenario = None
        self.selected_scenario_obj = None  
        self.selected_video = None
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (HomePage, SelectScenarioPage, VideoSelectionPage, SimulationScreenPage, ResultsPage, MedicinesPage, DiagnosisTrainerPage, CalibrationPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
