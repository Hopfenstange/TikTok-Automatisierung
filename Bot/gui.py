import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from login import login_tiktok
from follow import follow_users
from messages import send_message
from planner import plan_post
from stats import get_stats
import threading
import json

class TikTokBotGUI:
    def __init__(self, root):
        self.root = root
        root.title("TikTok Bot")

        self.tab_control = ttk.Notebook(root)
        self.tab_follow = ttk.Frame(self.tab_control)
        self.tab_message = ttk.Frame(self.tab_control)
        self.tab_plan = ttk.Frame(self.tab_control)
        self.tab_stats = ttk.Frame(self.tab_control)
        self.tab_settings = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_follow, text='Folgen')
        self.tab_control.add(self.tab_message, text='Nachrichten')
        self.tab_control.add(self.tab_plan, text='Planer')
        self.tab_control.add(self.tab_stats, text='Statistik')
        self.tab_control.add(self.tab_settings, text='Einstellungen')
        self.tab_control.pack(expand=1, fill='both')

        self.create_follow_tab()
        self.create_message_tab()
        self.create_plan_tab()
        self.create_stats_tab()
        self.create_settings_tab()

        self.driver = None
        self.blacklist = []
        self.load_blacklist()
        self.load_settings()

    def create_follow_tab(self):
        frame = self.tab_follow
        tk.Label(frame, text="Hashtag (ohne #):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.hashtag_entry = tk.Entry(frame)
        self.hashtag_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.follow_button = tk.Button(frame, text="Folgen starten", command=self.start_follow_thread)
        self.follow_button.grid(row=0, column=2, padx=5, pady=5)

        self.follow_log = tk.Text(frame, height=15, width=60)
        self.follow_log.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def create_message_tab(self):
        frame = self.tab_message
        tk.Label(frame, text="Benutzername:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.msg_user_entry = tk.Entry(frame)
        self.msg_user_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(frame, text="Nachricht:").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        self.msg_text = tk.Text(frame, height=5, width=40)
        self.msg_text.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.msg_send_button = tk.Button(frame, text="Nachricht senden", command=self.send_message_thread)
        self.msg_send_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.msg_log = tk.Text(frame, height=10, width=60)
        self.msg_log.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_plan_tab(self):
        frame = self.tab_plan
        tk.Label(frame, text="Videodatei:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.video_path_entry = tk.Entry(frame, width=40)
        self.video_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.browse_button = tk.Button(frame, text="Datei auswählen", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Beschreibung:").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        self.plan_desc_text = tk.Text(frame, height=5, width=40)
        self.plan_desc_text.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(frame, text="Datum (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.plan_date_entry = tk.Entry(frame)
        self.plan_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(frame, text="Uhrzeit (HH:MM):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.plan_time_entry = tk.Entry(frame)
        self.plan_time_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.plan_button = tk.Button(frame, text="Post planen", command=self.plan_post_action)
        self.plan_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.plan_log = tk.Text(frame, height=10, width=60)
        self.plan_log.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def create_stats_tab(self):
        frame = self.tab_stats
        self.stats_button = tk.Button(frame, text="Statistik aktualisieren", command=self.update_stats_thread)
        self.stats_button.grid(row=0, column=0, padx=5, pady=5)

        self.stats_text = tk.Text(frame, height=15, width=60)
        self.stats_text.grid(row=1, column=0, padx=5, pady=5)

    def create_settings_tab(self):
        frame = self.tab_settings
        tk.Label(frame, text="E-Mail:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(frame, text="Passwort:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.pw_entry = tk.Entry(frame, show='*', width=30)
        self.pw_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(frame, text="Blacklist (ein Benutzername pro Zeile):").grid(row=2, column=0, padx=5, pady=5, sticky='ne')
        self.blacklist_text = tk.Text(frame, height=10, width=40)
        self.blacklist_text.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.save_settings_button = tk.Button(frame, text="Einstellungen speichern", command=self.save_settings)
        self.save_settings_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.load_settings_button = tk.Button(frame, text="Einstellungen laden", command=self.load_settings)
        self.load_settings_button.grid(row=4, column=0, columnspan=2)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Video Dateien", "*.mp4;*.mov;*.avi")])
        if path:
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, path)

    def start_follow_thread(self):
        threading.Thread(target=self.follow_users_action, daemon=True).start()

    def follow_users_action(self):
        hashtag = self.hashtag_entry.get().strip()
        if not hashtag:
            messagebox.showerror("Fehler", "Bitte Hashtag eingeben.")
            return

        if not self.email_entry.get() or not self.pw_entry.get():
            messagebox.showerror("Fehler", "Bitte Login-Daten in Einstellungen eingeben.")
            return

        self.log_follow("Starte Login...")
        try:
            self.driver = login_tiktok(self.email_entry.get(), self.pw_entry.get())
        except Exception as e:
            self.log_follow(f"Login fehlgeschlagen: {e}")
            return

        self.load_blacklist()
        self.log_follow(f"Starte Folgen mit Hashtag: #{hashtag}")

        try:
            follow_users(self.driver, self.blacklist, hashtag, log_callback=self.log_follow)
        except Exception as e:
            self.log_follow(f"Fehler beim Folgen: {e}")

    def log_follow(self, message):
        self.follow_log.insert(tk.END, message + "\\n")
        self.follow_log.see(tk.END)

    def send_message_thread(self):
        threading.Thread(target=self.send_message_action, daemon=True).start()

    def send_message_action(self):
        user = self.msg_user_entry.get().strip()
        text = self.msg_text.get("1.0", tk.END).strip()

        if not user or not text:
            messagebox.showerror("Fehler", "Bitte Benutzername und Nachricht eingeben.")
            return

        if not self.driver:
            if not self.email_entry.get() or not self.pw_entry.get():
                messagebox.showerror("Fehler", "Bitte Login-Daten in Einstellungen eingeben.")
                return
            self.log_message("Starte Login...")
            try:
                self.driver = login_tiktok(self.email_entry.get(), self.pw_entry.get())
            except Exception as e:
                self.log_message(f"Login fehlgeschlagen: {e}")
                return

        self.log_message(f"Sende Nachricht an {user}...")
        try:
            send_message(self.driver, user, text, log_callback=self.log_message)
            self.log_message("Nachricht gesendet.")
        except Exception as e:
            self.log_message(f"Fehler beim Senden: {e}")

    def log_message(self, message):
        self.msg_log.insert(tk.END, message + "\\n")
        self.msg_log.see(tk.END)

    def plan_post_action(self):
        video_path = self.video_path_entry.get().strip()
        desc = self.plan_desc_text.get("1.0", tk.END).strip()
        date = self.plan_date_entry.get().strip()
        time_str = self.plan_time_entry.get().strip()

        if not video_path or not desc or not date or not time_str:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.")
            return

        try:
            plan_post(video_path, desc, date, time_str, log_callback=self.log_plan)
        except Exception as e:
            self.log_plan(f"Fehler beim Planen: {e}")

    def log_plan(self, message):
        self.plan_log.insert(tk.END, message + "\\n")
        self.plan_log.see(tk.END)

    def update_stats_thread(self):
        threading.Thread(target=self.update_stats_action, daemon=True).start()

    def update_stats_action(self):
        if not self.driver:
            if not self.email_entry.get() or not self.pw_entry.get():
                messagebox.showerror("Fehler", "Bitte Login-Daten in Einstellungen eingeben.")
                return
            self.log_stats("Starte Login...")
            try:
                self.driver = login_tiktok(self.email_entry.get(), self.pw_entry.get())
            except Exception as e:
                self.log_stats(f"Login fehlgeschlagen: {e}")
                return

        self.log_stats("Lade Statistiken...")
        try:
            stats = get_stats(self.driver)
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert(tk.END, stats)
        except Exception as e:
            self.log_stats(f"Fehler beim Laden der Statistik: {e}")

    def log_stats(self, message):
        self.stats_text.insert(tk.END, message + "\\n")
        self.stats_text.see(tk.END)

    def save_settings(self):
        settings = {
            "email": self.email_entry.get(),
            "password": self.pw_entry.get(),
            "blacklist": self.blacklist_text.get("1.0", tk.END).strip().split("\\n")
        }
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        messagebox.showinfo("Gespeichert", "Einstellungen wurden gespeichert.")

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, settings.get("email", ""))
            self.pw_entry.delete(0, tk.END)
            self.pw_entry.insert(0, settings.get("password", ""))
            self.blacklist_text.delete("1.0", tk.END)
            self.blacklist_text.insert("1.0", "\\n".join(settings.get("blacklist", [])))
            self.blacklist = [u.strip() for u in settings.get("blacklist", []) if u.strip()]
        except Exception:
            pass

    def load_blacklist(self):
        try:
            with open("blacklist.json", "r", encoding="utf-8") as f:
                self.blacklist = json.load(f)
            self.blacklist_text.delete("1.0", tk.END)
            self.blacklist_text.insert("1.0", "\\n".join(self.blacklist))
        except Exception:
            self.blacklist = []

def start_gui():
    root = tk.Tk()
    app = TikTokBotGUI(root)
    root.mainloop()
