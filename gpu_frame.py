import platform
import customtkinter as ctk
import GPUtil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

if platform.system().lower() == "windows":
    import wmi

darker_lightblue = "#468284"


def get_gpu_info():
    system = platform.system().lower()

    if "windows" in system:
        try:
            w = wmi.WMI(namespace="root\\CIMv2")
            gpu_info = w.query("SELECT * FROM Win32_VideoController")
            if gpu_info:
                gpu = gpu_info[0]
                return {
                    "gpu_name": gpu.Name,
                    "device_count": 1,
                    "total_memory": round(int(gpu.AdapterRAM) / 1024 ** 3, 2),
                }
        except Exception as e:
            print(f"WMI detection error: {e}")

    elif "linux" in system:
        try:
            import subprocess
            output = subprocess.check_output(["lshw", "-C", "display"], text=True)
            gpu_name = "Unknown"
            for line in output.split("\n"):
                if "product:" in line:
                    gpu_name = line.split(":")[1].strip()
                    break
            return {
                "gpu_name": gpu_name,
                "device_count": 1,
                "total_memory": "Unavailable",
            }
        except FileNotFoundError:
            print("lshw not installed. Install with: sudo apt install lshw")
        except Exception as e:
            print(f"Linux GPU detection error: {e}")

    return {
        "gpu_name": "Undetected",
        "device_count": 0,
        "total_memory": "Unavailable",
    }


class GPUFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.contents_frame = ctk.CTkFrame(self, fg_color="white")
        self.contents_frame.grid(row=0, column=0, sticky="nsew")

        gpu_info = get_gpu_info()

        self.create_gpu_labels(gpu_info)
        self.gpu_usage_data = []

        self.create_gpu_plot()

        self.contents_frame.grid_columnconfigure(0, weight=1)
        self.contents_frame.grid_columnconfigure(1, weight=0)
        self.contents_frame.grid_rowconfigure(4, weight=1)

        self.after(1000, self.update)

    def create_gpu_labels(self, gpu_info):
        self.gpu_label = ctk.CTkLabel(
            self.contents_frame,
            text="GPU Usage Monitor",
            font=("Segoe UI", 18, "bold"),
            text_color="darkblue",
        )

        self.gpu_name_label = ctk.CTkLabel(
            self.contents_frame,
            text=f"{gpu_info['gpu_name']}",
            font=("Segoe UI", 13, "normal"),
            text_color="blue",
        )

        self.device_count_label = ctk.CTkLabel(
            self.contents_frame,
            text=f"Device Count: {gpu_info['device_count']}",
            font=("Segoe UI", 13, "italic"),
            text_color="gray",
        )

        self.total_memory_label = ctk.CTkLabel(
            self.contents_frame,
            text=f"Total Memory: {gpu_info['total_memory']} GB",
            font=("Segoe UI", 13, "italic"),
            text_color="green",
        )

        self.gpu_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.gpu_name_label.grid(row=1, column=0, columnspan=2, sticky="nw", padx=10, pady=5)
        self.device_count_label.grid(row=2, column=0, columnspan=2, sticky="nw", padx=10, pady=5)
        self.total_memory_label.grid(row=3, column=0, columnspan=2, sticky="nw", padx=10, pady=5)

    def create_gpu_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("white")
        self.ax.tick_params(axis="x", colors="gray")
        self.ax.tick_params(axis="y", colors="gray")
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks(range(0, 101, 10))
        self.ax.set_ylabel("% Utilization", color="gray", fontsize=10)
        self.ax.set_xticklabels([])

        self.ax.set_xlabel("Last 60 seconds", color="gray", fontsize=10)
        self.ax.spines["top"].set_color(darker_lightblue)
        self.ax.spines["right"].set_color(darker_lightblue)
        self.ax.spines["bottom"].set_color(darker_lightblue)
        self.ax.spines["left"].set_color(darker_lightblue)
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        self.line, = self.ax.plot([0] * 60, color=darker_lightblue, linewidth=0.8)

        self.canvas = FigureCanvasTkAgg(self.figure, self.contents_frame)
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


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    gpu_frame = GPUFrame(root)
    gpu_frame.pack(fill="both", expand=True)
    root.mainloop()
