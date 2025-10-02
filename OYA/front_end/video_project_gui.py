import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

video_metadata = {
    "title": "",
    "description": "",
    "tags": "",
    "duration": "",
    "goal_upload_date": "",
    "thumbnail_path": "",
}

folder_templates = {
    "default": [
        "Raw Clips", "Music", "Screenshots", "Voiceovers",
        "Sound Effects", "Thumbnails", "Final Export"
    ],
    "custom": []
}

class VideoProjectApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Video Project Organizer")
        self.geometry("700x600")

        self.metadata_fields = {}
        self.selected_location = os.getcwd()

        self.build_ui()

    def build_ui(self):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        ctk.CTkLabel(frame, text="Title").pack()
        self.metadata_fields["title"] = ctk.CTkEntry(frame, placeholder_text="Enter title")
        self.metadata_fields["title"].pack(pady=5)

        # Description
        ctk.CTkLabel(frame, text="Description").pack()
        self.metadata_fields["description"] = ctk.CTkTextbox(frame, height=80)
        self.metadata_fields["description"].pack(pady=5)

        # Tags
        ctk.CTkLabel(frame, text="Tags (comma-separated)").pack()
        self.metadata_fields["tags"] = ctk.CTkEntry(frame)
        self.metadata_fields["tags"].pack(pady=5)

        # Duration
        ctk.CTkLabel(frame, text="Duration (e.g. 3:30)").pack()
        self.metadata_fields["duration"] = ctk.CTkEntry(frame)
        self.metadata_fields["duration"].pack(pady=5)

        # Upload Date
        ctk.CTkLabel(frame, text="Goal Upload Date").pack()
        self.metadata_fields["goal_upload_date"] = ctk.CTkEntry(frame)
        self.metadata_fields["goal_upload_date"].pack(pady=5)

        # Thumbnail Button
        self.thumbnail_button = ctk.CTkButton(frame, text="Select Thumbnail", command=self.select_thumbnail)
        self.thumbnail_button.pack(pady=10)

        # Folder Template Dropdown
        ctk.CTkLabel(frame, text="Folder Template").pack()
        self.template_selector = ctk.CTkOptionMenu(frame, values=list(folder_templates.keys()))
        self.template_selector.pack(pady=5)

        # Location Button
        self.location_button = ctk.CTkButton(frame, text="Select Save Location", command=self.select_save_location)
        self.location_button.pack(pady=5)

        # Create Project Button
        self.create_button = ctk.CTkButton(frame, text="Create Project", command=self.create_project)
        self.create_button.pack(pady=20)

    def select_thumbnail(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            video_metadata["thumbnail_path"] = path
            self.thumbnail_button.configure(text=os.path.basename(path))

    def select_save_location(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_location = folder
            self.location_button.configure(text=os.path.basename(folder))

    def create_project(self):
        # Collect metadata
        for key, widget in self.metadata_fields.items():
            if isinstance(widget, ctk.CTkTextbox):
                video_metadata[key] = widget.get("1.0", "end").strip()
            else:
                video_metadata[key] = widget.get().strip()

        if not video_metadata["title"]:
            messagebox.showwarning("Missing Info", "Please enter a project title.")
            return

        selected_template = self.template_selector.get()
        folders = folder_templates.get(selected_template, [])
        root_folder = os.path.join(self.selected_location, video_metadata["title"])

        try:
            os.makedirs(root_folder, exist_ok=True)
            for folder in folders:
                os.makedirs(os.path.join(root_folder, folder), exist_ok=True)

            with open(os.path.join(root_folder, "metadata.json"), "w") as f:
                json.dump(video_metadata, f, indent=4)

            messagebox.showinfo("Success", f"Project '{video_metadata['title']}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")


if __name__ == "__main__":
    app = VideoProjectApp()
    app.mainloop()
