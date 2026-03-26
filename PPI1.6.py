import customtkinter as ctk
from tkinter import filedialog, messagebox
import json, os
import platform
import zipfile
from urllib.request import urlopen
from urllib.parse import quote

main = ctk.CTk()
main.title("Planet Pack Installer 1.6")
main.geometry("1200x800")
root = ctk.CTkScrollableFrame(main, orientation="vertical")
root.pack(fill="both", expand=True)

data = None
currentos = platform.system()
with open("sfs_dir.txt", "r") as r:
    data2 = json.load(r)
    filepath = data2.get("filepath")

def extract_planet_pack(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            if member.is_dir():
                continue
            
            original_path = member.filename 
            
            if original_path.lower().startswith("system/"):
                new_name = original_path[7:] 
            else:
                new_name = original_path

            extract_to = os.path.dirname(zip_path)
            target_path = os.path.join(extract_to, new_name)

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

    os.remove(zip_path)

def get_descriptions():
    global data
    gitfile = urlopen("https://raw.githubusercontent.com/ilikespace9901/PlanetPackDatabase/main/packs.json")
    data = json.load(gitfile)

def ask_dir():
    def create_dir():
        global filepath
        filepath = filedialog.askdirectory()
        data = {
            "filepath": f"{filepath}"
        }
        with open("sfs_dir.txt", "w+") as w:
            w.write(json.dumps(data))
    if not os.path.exists("sfs_dir.txt"):
        create_dir()
    if os.path.getsize("sfs_dir.txt") == 0:
        create_dir()
        
def createbtn():
    def download_planetpack():
        filename2 = quote(data["planet_packs"]["file"])
        zipfile = urlopen(f"https://raw.githubusercontent.com/ilikespace9901/PlanetPackDatabase/main/{filename2}")
        with open(f"{data["planet_packs"]["file"]}", "wb") as f:
            f.write(zipfile)
    for planets in data["planet_packs"]:
        name = planets["name"]
        author = planets["author"]
        version = planets["version"]
        description = planets["description"]
        size = planets["size"]
        filename = planets["file"]
        compat = planets["compat"]
        def download_planetpack(p=planets):
            if currentos == "Android" or currentos == "iOS":
                filename2 = quote(p["file"])
                zipfile = urlopen(f"https://raw.githubusercontent.com/ilikespace9901/PlanetPackDatabase/main/{filename2}")
                zipcontent = zipfile.read()
                with open(f"{filepath}/Custom Solar Systems/{p["file"]}", "w") as f:
                    f.write(zipcontent)
                extract_planet_pack(f"{filepath}/Custom Solar Systems/{p["file"]}")
            elif currentos == "Windows" or currentos == "Darwin":
                filename2 = quote(p["file"])
                zipfile = urlopen(f"https://raw.githubusercontent.com/ilikespace9901/PlanetPackDatabase/main/{filename2}")
                zipcontent = zipfile.read()
                with open(f"{filepath}/Spaceflight Simulator_Data/Custom Solar Systems/{p["file"]}", "wb") as f:
                    f.write(zipcontent)
                extract_planet_pack(f"{filepath}/Spaceflight Simulator_Data/Custom Solar Systems/{p["file"]}")
        ctk.CTkButton(root, text=f"{name}\n{author}\n{version}\n{description}\n{size}\n{filename}\n{compat}", command=download_planetpack).pack(side="top", fill="x")

get_descriptions()
ask_dir()
createbtn()

main.mainloop()