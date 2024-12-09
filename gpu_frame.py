import customtkinter as ctk
import GPUtil
import wmi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

darker_lightblue = "#468284"

def get_gpu_info():
    try:
        w = wmi.WMI(namespace="root\\CIMv2")
        gpu_info = w.query("SELECT * FROM Win32_VideoController")
        if gpu_info:
            gpu = gpu_info[0]
            return {
                "gpu_name": gpu.Name,
                "device_count": 1,
                "total_memory": round(int(gpu.AdapterRAM) / 1024 ** 3, 2),  # Convert bytes to GB
            }
        else:
            print("WMI cannot detect a GPU")
    except Exception as e:
        print(f"WMI detection error: {e}")
    
    return {
        "gpu_name": "Undetected",
        "device_count": 0,
        "total_memory": "Unavailable",
    }

class GPUFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")
        
        self.grid_columnconfigure(0, weight=1)  # cpuinfo
        self.grid_rowconfigure(0, weight=1)
        
        gpu_info = get_gpu_info()
        
        self.create_gpu_labels(gpu_info)
        self.gpu_usage_data = []

        self.create_gpu_plot()

        self.after(1000, self.update)

    def create_gpu_labels(self, gpu_info):
        self.title_label = ctk.CTkLabel(
            self, text="GPU Info", font=("Segoe UI", 18, "bold"), text_color="darkblue"
        )
        self.title_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.gpu_name_label = ctk.CTkLabel(
            self,
            text=f"GPU Name: {gpu_info['gpu_name']}",
            font=("Segoe UI", 14),
            text_color="black",
        )
        self.gpu_name_label.grid(row=1, column=0, sticky='nw', padx=10, pady=5)

        self.device_count_label = ctk.CTkLabel(
            self,
            text=f"Device Count: {gpu_info['device_count']}",
            font=("Segoe UI", 14),
            text_color="black",
        )
        self.device_count_label.grid(row=2, column=0, sticky="nw", padx=10, pady=5)

        self.total_memory_label = ctk.CTkLabel(
            self,
            text=f"Total Memory: {gpu_info['total_memory']} GB",
            font=("Segoe UI", 14),
            text_color="black",
        )
        self.total_memory_label.grid(row=3, column=0, sticky="nw", padx=10, pady=5)

    def create_gpu_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("white")
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.ax.set_ylabel("% Utilization", color="gray", fontsize=10)
        self.ax.set_xticklabels([])

        self.ax.set_xlabel("Last 60 seconds", color="gray", fontsize=10)
        self.ax.spines['top'].set_color(darker_lightblue)
        self.ax.spines['right'].set_color(darker_lightblue)
        self.ax.spines['bottom'].set_color(darker_lightblue)
        self.ax.spines['left'].set_color(darker_lightblue)
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        self.line, = self.ax.plot([0] * 60, color=darker_lightblue, linewidth=0.8)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

    def update(self):
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = gpus[0].memoryUtil * 100
        else:
            gpu_usage = 0
        
        self.gpu_usage_data.append(gpu_usage)
        if len(self.gpu_usage_data) > 60:
            self.gpu_usage_data.pop(0)

        self.update_plot()
        self.after(1000, self.update)  

    def update_plot(self):
        self.line.set_ydata(self.gpu_usage_data)
        self.line.set_xdata(range(len(self.gpu_usage_data)))

        self.canvas.draw()

    def update_gpu_labels(self, gpu_info):
        self.gpu_name_label.configure(text=f"GPU Name: {gpu_info['gpu_name']}")
        self.device_count_label.configure(text=f"Device Count: {gpu_info['device_count']}")
        self.total_memory_label.configure(text=f"Total Memory: {gpu_info['total_memory']} GB")

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    gpu_frame = GPUFrame(root)
    gpu_frame.pack(fill="both", expand=True)
    root.mainloop()
