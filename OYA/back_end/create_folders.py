import os, sys, json, shutil, subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from Template import folder_templates, video_metadata

# Constants
METADATA_FILE = "metadata.json"
LAST_PATH_FILE = "last_project_path.txt"

# Global Widgets/State Containers
custom_folder_entries = []

# These will be initialized in setup_ui()
project_type_var = None
project_name_var = None
folder_path_var = None
folder_count_var = None
selected_path_label = None
folder_name_container = None
main_frame = None
app = None


def dynamic_center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = screen_width // 4
    y = screen_height // 4
    width = screen_width // 2
    height = screen_height // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    return width


def select_folder():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        messagebox.showerror("Error", "No folder selected.")
        return
    folder_path_var.set(folder_path)
    selected_path_label.configure(text=f"Selected Folder Path: {folder_path}")


def generate_custom_folder_fields():
    for widget in custom_folder_entries:
        widget.destroy()
    custom_folder_entries.clear()

    val = folder_count_var.get().strip()

    if val.lower() == 'n/a':
        ctk.CTkButton(main_frame, text="Create Project", command=confirm_and_create).pack(pady=20)
        return

    try:
        count = int(val)
        if count <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number greater than zero or 'N/A'.")
        return

    folder_name_container.pack(pady=10, fill="x")
    for i in range(count):
        lbl = ctk.CTkLabel(folder_name_container, text=f"Folder #{i+1} Name:")
        lbl.pack(pady=2)
        ent = ctk.CTkEntry(folder_name_container)
        ent.pack(pady=2)
        custom_folder_entries.append(ent)

    ctk.CTkButton(main_frame, text="Create Project", command=confirm_and_create).pack(pady=20)


def confirm_and_create():
    pt = project_type_var.get()
    pn = project_name_var.get().strip()
    fp = folder_path_var.get().strip()

    if not pn or not fp:
        messagebox.showerror("Error", "Project name and folder path are required.")
        return

    proj_path = os.path.join(fp, f"OYA_{pn}")
    while os.path.exists(proj_path):
        pn += "1"
        proj_path = os.path.join(fp, f"OYA_{pn}")
    os.makedirs(proj_path, exist_ok=True)

    # Create folders
    if pt == "default":
        folders = folder_templates[pt]
    else:
        folders = []
        for entry in custom_folder_entries:
            name = entry.get().strip()
            if name == "n/a":
                messagebox.showwarning("Invalid Entry", "Please do not enter 'n/a' for custom folders.")
                return  
            if not name:
                messagebox.showerror("Error", "All folder names must be filled.")
                return
            folders.append(name)

    for name in folders:
        os.makedirs(os.path.join(proj_path, name), exist_ok=True)

    metadata = video_metadata if pt == "default" else folders
    with open(os.path.join(proj_path, METADATA_FILE), "w") as f:
        json.dump(metadata, f, indent=4)
    with open(LAST_PATH_FILE, "w") as f:
        f.write(proj_path)
    with open("custom_folders.txt", "w") as f:
        for folder in folders:
            f.write(f"{folder}, ")

    messagebox.showinfo("Success", f"{len(folders)} folders created at:\n{proj_path}")
    app.destroy()
    subprocess.run(["python", r"OYA//front_end//project_dashboard.py"])


def setup_ui():
    global app, main_frame, selected_path_label, folder_name_container
    global project_type_var, project_name_var, folder_path_var, folder_count_var

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("OYA Project Creation")
    dynamic_center_window(app)

    # ✅ MUST initialize variables AFTER root is created
    project_type_var = ctk.StringVar(value=list(folder_templates.keys())[0])
    project_name_var = ctk.StringVar()
    folder_path_var = ctk.StringVar()
    folder_count_var = ctk.StringVar()

    main_frame = ctk.CTkScrollableFrame(app, width=600, height=400, corner_radius=10)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    folder_name_container = ctk.CTkFrame(main_frame)

    # UI Layout
    ctk.CTkLabel(main_frame, text="Choose Project Type").pack(pady=2)
    ctk.CTkOptionMenu(main_frame, variable=project_type_var, values=list(folder_templates.keys())).pack(pady=5)

    ctk.CTkLabel(main_frame, text="Project Name").pack(pady=2)
    ctk.CTkEntry(main_frame, textvariable=project_name_var).pack(pady=5)

    ctk.CTkButton(main_frame, text="Select Root Folder", command=select_folder).pack(pady=2)
    selected_path_label = ctk.CTkLabel(main_frame, wraplength=500, text="")
    selected_path_label.pack(pady=2)

    ctk.CTkLabel(main_frame, text="If custom, enter folder count. If default, enter 'N/A'.").pack(pady=2)
    ctk.CTkEntry(main_frame, textvariable=folder_count_var).pack(pady=2)

    ctk.CTkButton(main_frame, text="Generate Folder Fields", command=generate_custom_folder_fields).pack(pady=5)

    app.mainloop()

if __name__ == "__main__":
    setup_ui()
