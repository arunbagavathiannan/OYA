import customtkinter as ctk
from tkinter import messagebox
import subprocess, os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def dynamic_center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = screen_width // 4
    y = screen_height // 4
    width = screen_width // 2
    height = screen_height // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    return width

class OYADashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OYA - Orphic YouTube Assistant")
        self.geometry("900x550")  # Temporary, will be overridden below
        self.minsize(800, 500)

        dynamic_center_window(self)  # 👈 Apply center logic here

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) #what

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a", width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(
            self.sidebar, 
            text="OYA Menu", 
            font=("Segoe UI", 20, "bold"), 
            text_color="#00BFFF"
        ).pack(pady=(30, 20))

        self.sidebar_buttons = [
            ("🏠 Dashboard", self.dummy),
            ("👤 Account", self.open_account_popup),
            ("⚙️ Settings", self.dummy),
            ("💳 Subscription", self.dummy)
        ]

        for name, cmd in self.sidebar_buttons:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=name, 
                corner_radius=10, 
                hover_color="#005f87", 
                command=cmd
            )
            btn.pack(pady=10, padx=20, fill="x")

        # Main Area
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=15, border_width=2, border_color="#444", fg_color="#111"
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        self.setup_main_dashboard()

    def setup_main_dashboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.main_frame, 
            text="Welcome to OYA ✨", 
            font=("Segoe UI", 26, "bold"), 
            text_color="#00BFFF"
        ).pack(pady=(40, 20))

        # Main action buttons
        ctk.CTkButton(
            self.main_frame,
            text="+ Create New Project",
            font=("Segoe UI", 18, "bold"),
            height=60,
            width=260,
            fg_color="#00BFFF",
            hover_color="#0080ff",
            text_color="white",
            command=self.create_new_project
        ).pack(pady=30)

        ctk.CTkButton(
            self.main_frame,
            text="📁 View Current Projects",
            font=("Segoe UI", 14),
            height=45,
            width=220,
            fg_color="#333",
            hover_color="#555",
            command=self.view_projects
        ).pack(pady=10)

    def create_new_project(self):
        try:
            self.destroy()
            subprocess.run(["python", "back_end//create_folders.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't run create_folder.py\n\n{str(e)}")

    def view_projects(self):
        messagebox.showinfo("Coming Soon", "Project viewer is under development.")

    def open_account_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Set Up Your OYA Account")
        popup.configure(fg_color="#1a1a1a")
        popup.resizable(False, False)

        dynamic_center_window(popup)  # 👈 Center the popup window too

        ctk.CTkLabel(popup, text="Welcome, Creator 🚀", font=("Segoe UI", 22, "bold"), text_color="#00BFFF").pack(pady=(20, 10))
        ctk.CTkLabel(popup, text="Your journey to better content starts now.\nHere’s your current score:", font=("Segoe UI", 13)).pack(pady=5)

        ctk.CTkLabel(popup, text="⭐ Creator Score: 42/100", font=("Segoe UI", 18, "bold"), text_color="#FFD700").pack(pady=10)

        ctk.CTkLabel(
            popup,
            text="✅ 3 videos uploaded this month\n✅ 1,532 total views\n🎯 Target: 5 videos next month",
            font=("Segoe UI", 12),
            text_color="#CCCCCC",
            justify="center"
        ).pack(pady=10)

        ctk.CTkButton(
            popup,
            text="🚀 Upgrade Score (Soon)",
            font=("Segoe UI", 14, "bold"),
            fg_color="#00BFFF",
            hover_color="#0080ff",
            text_color="white",
            width=200,
            command=lambda: messagebox.showinfo("Coming Soon", "AI-powered upgrades launching soon!")
        ).pack(pady=20)

    def dummy(self):
        messagebox.showinfo("Coming Soon", "This feature is under development.")

if __name__ == "__main__":
    app = OYADashboard()
    app.mainloop()
