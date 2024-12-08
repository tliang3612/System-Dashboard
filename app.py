import customtkinter as ctk
from cpu_frame import CPUFrame
from network_frame import NetworkFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("PC Dashboard")
root.geometry("960x540")

root.grid_columnconfigure(0, weight=1)  # cpu frame column
root.grid_columnconfigure(1, weight=1)  # network frame column
root.grid_rowconfigure(0, weight=1)

#cpu frame
cpu_frame = CPUFrame(root)
cpu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

#network frame - works kinda; scalings off
network_frame = NetworkFrame(root)
network_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


root.mainloop()
