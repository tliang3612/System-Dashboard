import customtkinter as ctk
from cpu_frame import CPUFrame
from memory_frame import MemoryFrame
from network_frame import NetworkFrame

ctk.set_appearance_mode("System")  # Use system appearance (Light/Dark)
ctk.set_default_color_theme("blue")  # Set color theme

# Create root window
root = ctk.CTk()
root.title("PC Dashboard")
root.geometry("960x540")

# Create a tab view for different frames
tab_view = ctk.CTkTabview(root, width=960, height=540)
tab_view.pack(fill="both", expand=True, padx=20, pady=20)

# Add CPU Monitor tab
cpu_tab = tab_view.add("CPU Monitor")
cpu_frame = CPUFrame(cpu_tab)
cpu_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add Memory Monitor tab
memory_tab = tab_view.add("Memory Monitor")
memory_frame = MemoryFrame(memory_tab)
memory_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add Network Monitor tab
network_tab = tab_view.add("Network Monitor")
network_frame = NetworkFrame(network_tab)
network_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Run the main event loop
root.mainloop()
