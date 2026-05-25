import tkinter as tk
from tkinter import ttk, scrolledtext
import requests


def fetch_page():
    url = url_entry.get()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    proxy_url = f"http://localhost:5000/proxy?url={url}"

    try:
        response = requests.get(proxy_url)
        output_box.config(state='normal')
        output_box.delete('1.0', tk.END)
        output_box.insert(tk.END, response.text)
        output_box.config(state='disabled')
    except Exception as e:
        output_box.config(state='normal')
        output_box.delete('1.0', tk.END)
        output_box.insert(tk.END, f"Error fetching page:\n{str(e)}")
        output_box.config(state='disabled')



root = tk.Tk()
root.title("Proxy GUI - TEAM 121")
root.geometry("700x500")

title_label = ttk.Label(root, text="Welcome to Our Proxy Server - TEAM121", font=("Arial", 16, "bold"))
title_label.pack(pady=10)


url_frame = ttk.Frame(root)
url_frame.pack(pady=5)

url_label = ttk.Label(url_frame, text="Enter URL:")
url_label.pack(side='left')

url_entry = ttk.Entry(url_frame, width=60)
url_entry.pack(side='left', padx=5)

fetch_button = ttk.Button(url_frame, text="Fetch Page", command=fetch_page)
fetch_button.pack(side='left')


output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
output_box.pack(padx=10, pady=10, fill='both', expand=True)
output_box.config(state='disabled')

root.mainloop()
