import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import json
import requests  # <-- Add this import for requests

# Main Window
main = tk.Tk()
main.title("Planet Pack Installer for 1.6")
main.geometry("1200x700")

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
        r.raise_for_status()  # Raise error if the request failed
        descriptions = json.loads(r.text)
        return descriptions  # Return the entire list (not categorized)
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
    with open("cache.json", "w") as file:
        json.dump(data, file)
    if folder_path == "":
        return

if not os.path.exists("cache.json"):
    file_notexist()
elif os.path.getsize("cache.json") == 0:
    file_notexist()

with open("cache.json", "r") as file:
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

# UI related code
label = tk.Label(main, text="PPI for 1.6", font=("Arial", 20))
label.pack(side="top", pady=30)

ScrollingCanvas = tk.Canvas(main)
ScrollingCanvas.pack(side="top", fill="both", expand=True)

ScrollBar = ttk.Scrollbar(ScrollingCanvas, orient="vertical", command=ScrollingCanvas.yview)
ScrollingCanvas.configure(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side="right", fill="y")

ModsFrame = ttk.Frame(ScrollingCanvas, style="Mods.TFrame")
ScrollingCanvas.create_window((0, 0), window=ModsFrame, anchor="nw")
ModsFrame.bind("<Configure>", lambda event, canvas=ScrollingCanvas: canvas.configure(scrollregion=canvas.bbox("all")))
ModsFrame.pack(side="top", fill="both")

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
            compat = planet.get("compat", "Unknown compatible versiom")
            
            button_text = f"{planet_name} by {planet_author}\nDescription: {planet_desc}\nsize: {planet_fileSize}, version: {planet_version}\ncompatible with version {compat}"
            button = ttk.Button(ModsFrame, style="Mods.TButton", text=button_text)
            button.pack(side="top", fill="x", pady=5)

create_buttons_from_descriptions()

ButtonFrame = ttk.Frame(main, style="Button.TFrame")
ButtonFrame.pack(side="bottom", fill="x", pady=20)

main.mainloop()