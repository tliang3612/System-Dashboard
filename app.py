import customtkinter as ctk

from alerts_frame import AlertsFrame
from cpu_frame import CPUFrame
from gpu_frame import GPUFrame
from memory_frame import MemoryFrame
from network_frame import NetworkFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("PC Dashboard")
root.geometry("960x540")

root.grid_columnconfigure(0, weight=1)  # cpu frame column
root.grid_columnconfigure(1, weight=1)  # network frame column
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

#cpu frame
cpu_frame = CPUFrame(root)
cpu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

#network frame - works kinda; scalings off
network_frame = NetworkFrame(root)
network_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

gpu_frame = GPUFrame(root)
gpu_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

memory_frame = MemoryFrame(root)
memory_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

#alerts frame
alerts_frame = AlertsFrame(root, cpu_frame=cpu_frame, gpu_frame=gpu_frame, memory_frame=memory_frame)
alerts_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)


root.mainloop()
