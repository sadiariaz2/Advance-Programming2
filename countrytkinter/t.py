import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import pygame  

pygame.mixer.init()

def play_music():
    try:
        pygame.mixer.music.load("game-music.mp3")  
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play(-1) 
    except Exception as e:
        print(f"Error playing music: {e}")

def fetch_and_display_flag(flag_url, label):
    if not flag_url:
        label.config(image='', text='No flag available')
        return
    
    try:
        response = requests.get(flag_url, timeout=10)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((150, 100), Image.LANCZOS)
        flag_image = ImageTk.PhotoImage(img)
        label.config(image=flag_image, text='')
        label.image = flag_image
    except Exception as e:
        label.config(image='', text='Error loading flag')

def get_exchange_rate(currency_code):
    if not currency_code:
        return "N/A"

    url = "https://api.exchangerate.host/latest?base=USD"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        rates = data.get("rates", {})
        return f"1 USD = {rates.get(currency_code, 'N/A')} {currency_code}"
    except Exception:
        return "N/A"

def search_country():
    country_name = country_entry.get().strip()
    if not country_name:
        messagebox.showwarning("Input Required", "Please enter a country name.")
        return
    
    url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if response.status_code != 200 or not isinstance(data, list):
            messagebox.showinfo("Not Found", "No country found. Please check the name and try again.")
            return
        
        country = data[0]
        
        name_label.config(text="Country: " + country.get("name", {}).get("common", "N/A"))
        capital_label.config(text="Capital: " + ", ".join(country.get("capital", ["N/A"])))
        region_label.config(text="Region: " + country.get("region", "N/A"))
        subregion_label.config(text="Subregion: " + country.get("subregion", "N/A"))
        population_label.config(text="Population: " + f"{country.get('population', 'N/A'):,}")
        
        currency_info = country.get("currencies", {})
        if currency_info:
            currency_code = list(currency_info.keys())[0]
            currency_label.config(text="Currency: " + ", ".join([f"{v['name']} ({k})" for k, v in currency_info.items()]))
        else:
            currency_code = None
            currency_label.config(text="Currency: N/A")
        
        exchange_rate = get_exchange_rate(currency_code)
        exchange_rate_label.config(text="Exchange Rate: " + exchange_rate)

        language_info = country.get("languages", {})
        languages_label.config(text="Languages: " + ", ".join(language_info.values()) if language_info else "N/A")
        
        idd_info = country.get("idd", {})
        calling_code_label.config(text="Calling Code: +" + str(idd_info.get("root", "") + "".join(idd_info.get("suffixes", [""]))) if idd_info else "N/A")

        fetch_and_display_flag(country.get("flags", {}).get("png", ""), flag_label)
        
    except Exception:
        messagebox.showinfo("Error", "An error occurred while fetching country details.")

root = tk.Tk()
root.title("Country Search App")
root.geometry("600x700")
root.configure(bg="#CFD6C4")  # Main outer box background

play_music()

title_label = tk.Label(root, text="🌍 Country Explorer", font=("Arial", 18, "bold"), bg="#131311", fg="#FFFFFF")  # White text
title_label.pack(pady=15)

frame = tk.Frame(root, bg="#294D61", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)  # Search field & result box
frame.pack(pady=10)

entry_frame = tk.Frame(frame, bg="#294D61")
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Enter Country Name:", font=("Arial", 12), bg="#294D61", fg="#FFFFFF").pack(side=tk.LEFT)

country_entry = ttk.Entry(entry_frame, font=("Arial", 12), width=20)
country_entry.pack(side=tk.LEFT, padx=5)

search_button = ttk.Button(frame, text="🔍 Search", command=search_country)
search_button.pack(pady=10)

data_frame = tk.Frame(frame, bg="#294D61")
data_frame.pack()

name_label = tk.Label(data_frame, text="", font=("Arial", 12, "bold"), bg="#294D61", fg="#FFFFFF")
name_label.pack()

capital_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
capital_label.pack()

region_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
region_label.pack()

subregion_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
subregion_label.pack()

population_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
population_label.pack()

currency_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
currency_label.pack()

exchange_rate_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
exchange_rate_label.pack()

languages_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
languages_label.pack()

calling_code_label = tk.Label(data_frame, text="", font=("Arial", 12), bg="#294D61", fg="#FFFFFF")
calling_code_label.pack()

flag_label = tk.Label(frame, text="", bg="#294D61")
flag_label.pack(pady=10)

tk.Label(root, text="✨ Developed by Sadia", font=("Arial", 10), bg="#131311", fg="#DCAB09").pack(pady=10)  # Yellow text

root.mainloop()