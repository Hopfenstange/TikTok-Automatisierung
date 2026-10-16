import tkinter as tk
from tkinter import messagebox
from login import login_tiktok
from follow import follow_users
import json

def start_bot():
    email = email_entry.get()
    pw = pw_entry.get()
    hashtag = hashtag_entry.get()

    if not email or not pw:
        messagebox.showerror("Fehler", "Bitte Email und Passwort eingeben.")
        return

    with open("blacklist.json", "r") as f:
        blacklist = json.load(f)

    try:
        driver = login_tiktok(email, pw)
        follow_users(driver, blacklist, hashtag)
    except Exception as e:
        messagebox.showerror("Fehler beim Starten", str(e))

root = tk.Tk()
root.title("TikTok Bot")

tk.Label(root, text="E-Mail:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(root, text="Passwort:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Label(root, text="Hashtag:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

email_entry = tk.Entry(root, width=30)
pw_entry = tk.Entry(root, show="*", width=30)
hashtag_entry = tk.Entry(root, width=30)
email_entry.grid(row=0, column=1, padx=5, pady=5)
pw_entry.grid(row=1, column=1, padx=5, pady=5)
hashtag_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Bot starten", command=start_bot).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
