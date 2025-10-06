import customtkinter as ctk
import subprocess
from tkinter import ttk
import textstat
import nltk, yake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import random as rd

# from back_end.create_folders import project_time (later)

"""
OYA Dashboard Theme:

- Appearance: dark mode, CustomTkinter 'blue' theme
- Main window bg: default dark (#111)
- Sidebar: #1a1a1a bg, 200px width, text #00BFFF (bright blue)
- Sidebar buttons: bg #1a1a1a, hover #005f87, text white
- Main frame: bg #111, border #444, radius 15
- Titles: Segoe UI, bold, blue #00BFFF
- Main buttons: blue #00BFFF fg, hover #0080ff, white text
- Secondary buttons: dark gray #333 fg, hover #555
- Popup bg: #1a1a1a, text colors blue (#00BFFF), gold (#FFD700), light gray (#CCC)
"""

# default themes
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProjectDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # make window
        self.title("Project Dashboard")
        self.minsize(600, 480)

        # center in the middle
        self.screen_width = self.winfo_screenwidth()
        self.screen_length = self.winfo_screenheight()
        self.x = (self.screen_width // 2) - (500)
        self.y = (self.screen_length // 2) - (500)
        self.geometry(f"1000x1000+{self.x}+{self.y}")

    def create_sidebar(self):

        # sidebar dimensions don't change based on widgets (propogation)
        sidebar = ctk.CTkFrame(
            self, 
            bg_color="#111111", 
            width=200, 
            height=800, 
            fg_color="#1a1a1a", 
            border_width=1, 
            border_color="#444444"
        )
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        # Button to back to First Dashboard
        def go_back():
            self.destroy()
            subprocess.run(["python", "front_end\\first_dashboard.py"])
            # Later on, add an option that saves all data when this function is called

        back_button = ctk.CTkButton(
            sidebar, 
            text="Back", 
            text_color="#00BFFF", 
            fg_color="#333333", 
            hover_color="#555555", 
            command=go_back
        )
        back_button.pack(pady=10)
        
        Progress_Label = ctk.CTkLabel(
            sidebar,
            font=("Segoe UI", 18, "bold"), 
            text="📊 Progress Bar", 
            text_color="#00BFFF"
        ).pack(pady=10)

        # Progress Chart Tinkering
        days_since_start = [a for a in range(1, 100) if a > 0]
        parts_completed = [a for a in range(1, 100) if a > 0]
        empty_list = []
        with open("OYA\\progress_bar_info.csv", "w") as f:
            f.write(empty_list)


        self.pb = ctk.CTkProgressBar(sidebar, width="220", height='14', fg_color="#1a1a1a", progress_color="#00b3ff")
        csv_info = pd.read_csv("progress_bar_info.csv")
        self.pb.configure()


        # Folder Outline View and clickability
        with open("OYA\\last_project_path.txt", "r") as file:
            project_folder = file.read().split("\\")[1]

        folder_title = ctk.CTkLabel(
            sidebar, 
            font=("Segoe UI", 18, "bold"), 
            text="📁 Folder View", 
            text_color="#00BFFF"
        ).pack(pady=10)

        folder_frame = ctk.CTkScrollableFrame(
            sidebar, 
            bg_color="#000000", 
            width=160, 
            height=200
        )
        folder_frame.pack(pady=10)

        folder_label = ctk.CTkLabel(
            folder_frame, 
            text=f"📁 {project_folder}", 
            text_color="#FFFFFF", 
            font=("Segoe UI", 10, "bold"), 
            anchor="w"
        ).pack(pady=5)

        with open("OYA\\custom_folders.txt", "r") as file:
            subfolders = file.read().split(", ")
        
        for folder in subfolders:
            ctk.CTkLabel(
                folder_frame, 
                text=f" {folder}", 
                text_color="#FFFFFF", 
                font=("Segoe UI", 14, "bold")
            ).pack(pady=15)

        SEO_Optimizer_Button = ctk.CTkButton(
            sidebar, 
            text="SEO Optimizer", 
            fg_color="#00BFFF", 
            font=("Segoe UI", 14, "bold"),
            command=self.create_SEO_Optimizer_UI
        )
        SEO_Optimizer_Button.pack(pady=10)

    # ---------------------- BUTTONS ------------------------
    
    # ----------------- SEO Optimizer -----------------------
    def create_SEO_Optimizer_UI(self):

        # create frame, and SEO Optimizing Widgets and entry fields inside for title
        main_frame = ctk.CTkFrame(
                self,
                width=800,
                height=800,
                fg_color="#080606",
                border_width=1,
                border_color="#101010"
            )
        main_frame.pack(fill="y", side="right")
        main_frame.pack_propagate(False)

        # input fields for title and description
        title = ctk.CTkLabel(
                main_frame,
                text="Your Title:",
                text_color="#FFFFFF",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
        self.title_entry = ctk.CTkTextbox(
            main_frame,
            width=500,
            height=30,
        )
        self.title_entry.pack(pady=5)
        self.title_feedback = ctk.CTkLabel(
                main_frame,
                font=("Segoe UI", 10, "bold"),
                text=""
            )
        self.title_feedback.pack()

        description = ctk.CTkLabel(
                main_frame,
                text="Your Description:",
                text_color="#FFFFFF",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
        self.description_entry = ctk.CTkTextbox(
                main_frame,
                width=500,
                height=150
            )
        self.description_entry.pack(pady=5)
        self.description_feedback = ctk.CTkLabel(
                main_frame,
                font=("Segoe UI", 10, "bold"),
                text=""
            )
        self.description_feedback.pack()

        transcript = ctk.CTkLabel(
                main_frame,
                text="Your Transcript:",
                text_color="#FFFFFF",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
        self.transcript_entry = ctk.CTkTextbox(
            main_frame,
            width=500,
            height=350,
        )
        self.transcript_entry.pack(pady=5)
        self.transcript_feedback = ctk.CTkLabel(
                main_frame,
                font=("Segoe UI", 10, "bold"),
                text=""
            )
        self.transcript_feedback.pack()

        self.feedbacks = [
            self.title_feedback, 
            self.description_feedback, 
            self.transcript_feedback
        ]

        self.entries = [
            self.title_entry,
            self.description_entry,
            self.transcript_entry
        ]

        self.names = [
            "title",
            "description",
            "transcript"
        ]

        check_button = ctk.CTkButton(
            main_frame,
            text="Check All",
            font=("Segoe UI", 20, "bold"),
            corner_radius=5,
            fg_color="#00BFFF",
            command=self.CheckAll
        )
        check_button.pack(pady=10)
    
    def CheckAll(self):

        for entry in self.entries: # Check

            # Convert
            entry1 = entry.get("1.0", "end-1c")
            
            # Check
            if entry1 == "":
                continue

        # Remove pre-existing feedback
        for label in self.feedbacks:
            label.configure(text="")
        
        # Lists and Prep
        nltk.download("punkt_tab")
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))
        power_words = ["ultimate", "best", "easy", "insane", "how-to", "proven", "shocking", "how to"]

        for name, content, feedback in zip(
            self.names, 
            [e.get("1.0", "end-1c") for e in self.entries],
            self.feedbacks
        ):
            if len(content) < 10:
                feedback.configure(text="Too short to analyze")
                continue

            # Readability
            r_score = textstat.flesch_reading_ease(content)
            r_score_feedback = ""
            if r_score < 30:
                r_score_feedback = "Too complicated; try using less complex words"

            # Keywords
            words = word_tokenize(content.lower())
            filtered_words = [w for w in words if w.isalpha() and w not in stop_words]

            # Emotional word usage
            used_power = [w for w in power_words if w in filtered_words]
            used_power_count = 0
            for u in used_power:
                used_power_count += 1
            power_word_feedback = ""
            if used_power:
                power_word_feedback = f"Power words: {', '.join(used_power)}"

            # Feedback
            feedback.configure(text=f"Readability score: {round(r_score, 2)} \n {r_score_feedback} \n {power_word_feedback}")

def run():
    app = ProjectDashboard()
    app.create_sidebar()
    app.mainloop()
if __name__ == "__main__":
    run()

# NEXT STEP: PROGRESSBAR + pandas information into CSV

# HOW TO INTEGRATE YT CHANNEL STATS INTO OYA