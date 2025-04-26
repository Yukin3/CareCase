# test_gui.py
import tkinter as tk

app = tk.Tk()
app.geometry("300x200")
tk.Label(app, text="✅ GUI is working!").pack(pady=20)
app.mainloop()
