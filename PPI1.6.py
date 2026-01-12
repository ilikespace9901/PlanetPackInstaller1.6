import tkinter as tk
from tkinter import filedialog
import os
import json

main = tk.Tk()
main.title("Planet Pack Installer for 1.6")
main.geometry("1200x700")

label = tk.Label(main, text="PPI for 1.6", font=("Arial", 20))
label.pack()

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
	
main.mainloop()
