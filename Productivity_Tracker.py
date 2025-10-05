import customtkinter as ctk
import psutil
import time
import threading
from plyer import notification
import ctypes
from ctypes import wintypes


# USER MODIFIES SETTINGS HERE (theyre constants)
BLACKLIST = ["youtube", "discord", "netflix", "reddit", "twitch", "spotify"]
CHECK_INTERVAL = 3
UNPRODUCTIVE_LIMIT = 2 # this is the time between nudges




# function for getting active apps
def get_active_app():
    
    # finding process IDs from your system
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow() 
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))


    # psutil to get processes
    try:
        process_name = psutil.Process(pid.value).name()
        return process_name
    except Exception:
        return None


# GUI with customtkinter
app = ctk.CTk()
app.title("Minimalist Productivity Tracker")
app.geometry("400x250")

title = ctk.CTkLabel(app, text="Productivity Tracker", font=("Calisto MT", 25, "bold"))
title.pack(pady=10)

prod_label = ctk.CTkLabel(app, text="Productive time: 0s", font=("Calisto MT", 14))
prod_label.pack(pady=5)

unprod_label = ctk.CTkLabel(app, text="Unproductive time: 0s", font=("Calisto MT", 14))
unprod_label.pack(pady=5)

current_label = ctk.CTkLabel(app, text="Current app: None", font=("Calisto MT", 12))
current_label.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Tracking...", font=("Calisto MT", 12))
status_label.pack(pady=5)


productive_time = 0
unproductive_timer = 0
total_unprod_time = 0

# productivity tracker
def tracker():
    global productive_time, total_unprod_time, unproductive_timer

    # loops constantly while active
    while True:

        # pull the active app
        current_app = get_active_app()

        if current_app:
            current_label.configure(text=f"Current app: {current_app}")

            # Check if app is unproductive
            if any(bad in current_app.lower() for bad in BLACKLIST):
                total_unprod_time += CHECK_INTERVAL
                unproductive_timer += CHECK_INTERVAL
                status_label.configure(text="Unproductive.", text_color="red")
            else:
                productive_time += CHECK_INTERVAL
                unproductive_timer = 0
                status_label.configure(text="Productive!", text_color="green")

            # Send nudge if unproductive too long
            if unproductive_timer >= UNPRODUCTIVE_LIMIT:
                notification.notify(
                    title = "Stay Focused!",
                    message = "You've been unproductive for a while. Refocus!",
                    timeout = 5
                )
                unproductive_timer = 0

            # update GUI
            prod_label.configure(text=f"Productive time: {productive_time}s")
            unprod_label.configure(text=f"Unproductive time: {total_unprod_time}s")

        # interval before recheck
        time.sleep(CHECK_INTERVAL)

# let program run in the background
threading.Thread(target=tracker, daemon=True).start()

app.mainloop()