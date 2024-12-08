import customtkinter as ctk
from cpu_frame import CPUFrame

ctk.set_appearance_mode("System")  # Use system appearance (Light/Dark)
ctk.set_default_color_theme("blue")  # Set color theme

root = ctk.CTk()
root.title("PC Dashboard")
root.geometry("960x540")

#cpu frame
cpu_frame = CPUFrame(root)
cpu_frame.pack(pady=20, padx=60, fill="both", expand = "true")

#network frame - works kinda; scalings off
network_frame = NetworkFrame(root)
network_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nsew")


root.mainloop()
