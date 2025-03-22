import tkinter as tk
from tkinter import Label, Button, Frame, Canvas
import requests
import ssl
import socket
from urllib.parse import urlparse

def check_ssl(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else 443
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()
                if certificate:
                    return "SSL Valid"
                else:
                    return "No Certificate"
    except Exception as e:
        return f"SSL Error: {str(e)}"

def check_website_status(url, label):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            ssl_status = check_ssl(url)
            label.config(text=f"{url} UP ({ssl_status})", bg="green", fg="white")
        else:
            label.config(text=f"{url} DOWN", bg="red", fg="white")
    except requests.exceptions.RequestException:
        label.config(text=f"{url} DOWN", bg="red", fg="white")

def monitor_websites():
    check_website_status("https://sukamarakab.go.id", label_widgets[0])
    check_website_status("https://kominfosandi.sukamarakab.go.id", label_widgets[1])
    check_website_status("https://e-bikon.sukamarakab.go.id", label_widgets[2])
    check_website_status("https://jdih.sukamarakab.go.id", label_widgets[3])
    check_website_status("https://siulankuda.sukamarakab.go.id", label_widgets[4])
    check_website_status("https://binakonstruksi.sukamarakab.go.id", label_widgets[5])
    check_website_status("https://dikbud.sukamarakab.go.id", label_widgets[6])
    check_website_status("https://bappeda.sukamarakab.go.id", label_widgets[7])
    check_website_status("https://disdukcapil.sukamarakab.go.id", label_widgets[8])
    check_website_status("https://dpmptsp.sukamarakab.go.id", label_widgets[9])
    check_website_status("https://epajak.sukamarakab.go.id", label_widgets[10])
    check_website_status("https://bpkad.sukamarakab.go.id", label_widgets[11])
    root.after(18000, monitor_websites)  # Cek ulang setiap 5 menit

def exit_app():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Website Monitor")
root.geometry("400x500")
root.config(bg="white")

# Buat canvas dan scrollbar
canvas = Canvas(root, borderwidth=0, bg="white")
frame = Frame(canvas, bg="white")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Judul monitoring
Label(frame, text="Website Monitoring", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

# Buat label untuk tiap website dan simpan dalam list untuk memudahkan update
urls = [
    "https://sukamarakab.go.id",
    "https://kominfosandi.sukamarakab.go.id",
    "https://e-bikon.sukamarakab.go.id",
    "https://jdih.sukamarakab.go.id",
    "https://siulankuda.sukamarakab.go.id",
    "https://binakonstruksi.sukamarakab.go.id",
    "https://dikbud.sukamarakab.go.id",
    "https://bappeda.sukamarakab.go.id",
    "https://disdukcapil.sukamarakab.go.id",
    "https://dpmptsp.sukamarakab.go.id",
    "https://epajak.sukamarakab.go.id",
    "https://bpkad.sukamarakab.go.id"
]
label_widgets = []
for url in urls:
    lbl = Label(frame, text="Checking...", font=("Arial", 10), width=50, height=2)
    lbl.pack(pady=3)
    label_widgets.append(lbl)

# Tombol keluar diletakkan di frame (bisa discroll bersama konten)
exit_button = Button(frame, text="Keluar", font=("Arial", 12), command=exit_app, bg="red", fg="white")
exit_button.pack(pady=10)

# Mulai monitoring
root.after(1000, monitor_websites)
root.mainloop()
