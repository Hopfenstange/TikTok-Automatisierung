import json
from datetime import datetime

def plan_post(video_path, description, date_str, time_str, log_callback=None):
    try:
        dt_str = date_str + " " + time_str
        post_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        now = datetime.now()
        if post_time <= now:
            if log_callback:
                log_callback("Fehler: Geplantes Datum/Uhrzeit liegt in der Vergangenheit.")
            return
        # Nur lokale Speicherung
        planned_posts = []
        try:
            with open("planned_posts.json", "r", encoding="utf-8") as f:
                planned_posts = json.load(f)
        except FileNotFoundError:
            pass
        planned_posts.append({
            "video_path": video_path,
            "description": description,
            "post_time": dt_str
        })
        with open("planned_posts.json", "w", encoding="utf-8") as f:
            json.dump(planned_posts, f, indent=4)
        if log_callback:
            log_callback(f"Post geplant für {dt_str}")
    except Exception as e:
        if log_callback:
            log_callback(f"Fehler beim Planen: {e}")
