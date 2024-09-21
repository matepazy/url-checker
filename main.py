import tkinter as tk
from tkinter import messagebox
import requests
import time

def scan_url():
    url = "https://www.virustotal.com/api/v3/urls"
    website = url_entry.get()
    payload = f"url={website}"
    headers = {
        "accept": "application/json",
        "x-apikey": "xxxx",
        "content-type": "application/x-www-form-urlencoded"
    }

    # Disable the scan button
    scan_button.config(state="disabled")
    # Display "Please wait" label
    please_wait_label.config(text="Kérlek várj...", fg="blue")

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        json_data = response.json()

        analysis_url = json_data["data"]["links"]["self"]

        # Send a GET request to the analysis URL
        analysis_response = requests.get(analysis_url, headers=headers)

        if analysis_response.status_code == 200:
            analysis_results = analysis_response.json()["data"]["attributes"]["results"]

            # Check the results for any harmful indicators
            is_harmful = any(result["category"] != "harmless" for result in analysis_results.values())

            # Update the result label
            if is_harmful:
                result_label.config(text="Ez az URL biztonságos.\nAjánlott, hogy újra lefuttasd a elemzést.", fg="green")
            else:
                result_label.config(text="Ez az URL veszélyes.\nAjánlott, hogy újra lefuttasd a elemzést.", fg="red")
                messagebox.showinfo("Figyelem!", "Lehet hogy HAMIS POZITÍV a teszt, szóval ajánlott ÚJRA LEFUTTATNI!")
        else:
            result_label.config(text="Hiba: Nem sikerül elérni az elemzést.", fg="orange")
    else:
        result_label.config(text="Hiba: Nem sikerült elemezni az URL-t.", fg="orange")

    # Re-enable the scan button
    scan_button.config(state="normal")
    # Hide "Please wait" label
    time.sleep(2)
    please_wait_label.config(text="")

# Create the main window
window = tk.Tk()
window.title("URL Scanner")
window.geometry("400x210")

# Create and pack the URL label and entry
url_label = tk.Label(window, text="Írd be a webcímet:", font=("Arial", 14))
url_label.pack(pady=10)

url_entry = tk.Entry(window, width=30, font=("Arial", 12))
url_entry.pack()

# Create and pack the scan button
scan_button = tk.Button(window, text="Elemzés", command=scan_url, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", padx=10, pady=5, bd=0)
scan_button.pack(pady=10)

# Create and pack the "Please wait" label
please_wait_label = tk.Label(window, text="", font=("Arial", 12))
please_wait_label.pack()

# Create and pack the result label
result_label = tk.Label(window, text="", font=("Arial", 16))
result_label.pack()

# Start the Tkinter event loop
window.mainloop()
