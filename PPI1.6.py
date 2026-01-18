import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import json
import requests

# Change this counter to be accurate
# Hours Wasted: 2

main = tk.Tk()
main.title("Planet Pack Installer for 1.6")
main.geometry("780x700")

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Mods.TFrame",
    foreground="white",
    background="#424242",
    padding=10
)
style.configure(
    "Mods.TButton",
    foreground="white",
    background="#424242",
    padding=10
)
style.configure(
    "Button.TFrame",
    foreground="white",
    background="#424242",
    padding=10
)
style.configure(
    "PPI.TFrame",
    foreground="white",
    background="#424242",
    padding=10
)

# Github Stuff
REPO = "ilikespace9901/PlanetPackDatabase"
DESCRIPTION = "packs.json"

# Functions
def fetch_descriptions():
    try:
        url = f"https://raw.githubusercontent.com/{REPO}/main/{DESCRIPTION}"
        r = requests.get(url)
        r.raise_for_status()
        descriptions = json.loads(r.text)
        return descriptions
    except Exception as e:
        print(f"Error fetching descriptions: {e}")
        return []

def download_file(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    return r.content

def file_notexist():
    folder_path = filedialog.askdirectory()
    data = {
        "path": folder_path
    }
    with open("sfs_dir.txt", "w") as file:
        json.dump(data, file)
    if folder_path == "":
        return

if not os.path.exists("sfs_dir.txt"):
    file_notexist()
elif os.path.getsize("sfs_dir.txt") == 0:
    file_notexist()

with open("sfs_dir.txt", "r") as file:
    data = json.load(file)
path = data["path"]

def installed():
    messagebox.showinfo(
        title="Installed a mod",
        message="You have installed a mod"
    )

def change_directory():
    file_path = "cache.json"
    os.remove(file_path)
    file_notexist()

# UI related shit

ScrollingCanvas = tk.Canvas(main)
ScrollingCanvas.pack(side="top", fill="both", expand=True)

ScrollBar = ttk.Scrollbar(ScrollingCanvas, orient="vertical", command=ScrollingCanvas.yview)
ScrollingCanvas.configure(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side="right", fill="y")

ModsFrame = ttk.Frame(ScrollingCanvas, style="Mods.TFrame")
ModsFrame.pack(fill="both", expand=True)
ScrollingCanvas.create_window((0, 0), window=ModsFrame, anchor="nw")

ModsFrame.bind("<Configure>", lambda event, canvas=ScrollingCanvas: canvas.configure(scrollregion=canvas.bbox("all")))

def create_buttons_from_descriptions():
    descriptions = fetch_descriptions()
    planet_packs = descriptions.get('planet_packs', [])
    if planet_packs:
        for planet in planet_packs:
            planet_name = planet.get("name", "Unknown Name")
            planet_author = planet.get("author", "Unknown Author")
            planet_desc = planet.get("description", "No description")
            planet_fileSize = planet.get("size", "Unknown file size")
            planet_version = planet.get("version", "Unknown version")
            compat = planet.get("compat", "Unknown compatible version")
            
            button_text = f"{planet_name} by {planet_author}\nDescription: {planet_desc}\nSize: {planet_fileSize}, Version: {planet_version}\nCompatible with: {compat}"
            button = ttk.Button(ModsFrame, style="Mods.TButton", text=button_text)
            button.pack(side="top", fill="x", pady=5)

create_buttons_from_descriptions()

main.mainloop()