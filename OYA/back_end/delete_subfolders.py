import os
import shutil as shut
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk() # open an instance of module
root.withdraw()  # take away the thingy

folder_path = filedialog.askdirectory(title="Select a Folder to delete the folders within it")

rel_path = rf"{folder_path}"
folder_name = os.path.basename(rel_path)
if rel_path:
    confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to permanently delete all folders in {folder_name}?")
    if confirmation:
        for dir in os.listdir(rel_path):
            check_path = os.path.join(rel_path, dir)
            if os.path.isdir(check_path):
                shut.rmtree(check_path)
        print("Folder and all its contents deleted.")
    else:
        print("Deletion aborted.")
else:
    print("No folder path detected.")