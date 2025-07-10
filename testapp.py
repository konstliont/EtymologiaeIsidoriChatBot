import tkinter as tk
from tkinter import ttk
from chat import get_response, bot_name
from PIL import Image, ImageTk
import sqlite3
import pandas as pd
import os

BG_COLOR = "#f4f4f4"
TEXT_COLOR = "#333"
FONT = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 12, "bold")

def send_message(event=None):
    msg = msg_entry.get()
    if not msg:
        return
    
    msg_entry.delete(0, tk.END)
    chat_text.configure(state=tk.NORMAL)
    chat_text.insert(tk.END, f"Tu: {msg}\n", "user")
    chat_text.insert(tk.END, f"{bot_name}: {get_response(msg)}\n", "bot")
    chat_text.configure(state=tk.DISABLED)
    chat_text.yview(tk.END)

def export_to_excel():
    conn = sqlite3.connect("chatbot_liberx.db")
    query = """
    SELECT tags.tag, responses.response 
    FROM tags 
    JOIN responses ON tags.id = responses.tag_id 
    WHERE tags.id >= 6
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    file_path = "etymology_export.xlsx"
    df.to_excel(file_path, index=False)
    os.system(f'open "{file_path}"')

# Παράθυρο
root = tk.Tk()
root.title("Chatbot Etymologiarum Liber X")
root.geometry("500x600")

# Κεφαλίδα
header_frame = tk.Frame(root, bg="#008080", height=50)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Etymologiarum Liber X", fg="white", bg="#008080", font=FONT_BOLD).pack(pady=10)

# Εικόνα
logo = Image.open("1-fe37d2e0.png").resize((80, 80), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image=logo)
logo_label.pack(pady=10)

# Περιοχή συνομιλίας
chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
chat_text = tk.Text(chat_frame, wrap=tk.WORD, bg="white", fg=TEXT_COLOR, font=FONT, state=tk.DISABLED)
chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(chat_frame, command=chat_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_text.config(yscrollcommand=scrollbar.set)
chat_text.tag_configure("user", foreground="#555", font=FONT_BOLD)
chat_text.tag_configure("bot", foreground="#555", font=FONT)

# Μήνυμα καλωσορίσματος
chat_text.configure(state=tk.NORMAL)
chat_text.insert(tk.END, f"{bot_name}: Loquamur! Quae verba quaeris?\n", "bot")
chat_text.configure(state=tk.DISABLED)

# Περιοχή εισαγωγής μηνυμάτων
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.X, padx=10, pady=5)
msg_entry = ttk.Entry(bottom_frame, font=FONT)
msg_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
msg_entry.bind("<Return>", send_message)
send_button = ttk.Button(bottom_frame, text="Αποστολή", command=send_message)
send_button.pack(side=tk.RIGHT)

# Κουμπί εξαγωγής
export_button = ttk.Button(root, text="Εξαγωγή σε Excel", command=export_to_excel)
export_button.pack(pady=10)


root.mainloop()

