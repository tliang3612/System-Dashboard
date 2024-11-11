import tkinter as tk
from cpu_frame import CPUFrame

root = tk.Tk()
root.title("PC Dashboard")
root.geometry("960x540")
root.configure(bg="white")

#cpu frame
cpu_frame = CPUFrame(root)
cpu_frame.grid(row=0, column=0, sticky="nsew")

#adaptive resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()