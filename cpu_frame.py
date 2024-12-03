import customtkinter as ctk
import psutil
import platform
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE


def get_cpu_info():
    # determine cpu name by going into
    cpu_name = None
    if platform.system() == "Windows":
        try:
            registry_key = OpenKey(HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") #get reference to first cpu registry key location
            cpu_name, reg = QueryValueEx(registry_key, "ProcessorNameString") #retrieve value of ProcessorNameString from the key to get the cpu name
        except Exception:
            cpu_name = "Unknown CPU"
    # untested
    # elif platform.system() == "Linux":
    #     try:
    #         with open("/proc/cpuinfo", "r") as f:
    #             for line in f:
    #                 if "model name" in line:
    #                     cpu_name = line.split(":")[1].strip()
    #                     break
        except Exception:
            cpu_name = "Unknown CPU"

    #get core counts
    cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    return {
        "cpu_name": cpu_name,
        "cores": cores,
        "logical_cores": logical_cores,
    }


class CPUFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        # get info about the cpu
        cpu_info = get_cpu_info()

        self.cpu_label = ctk.CTkLabel(self, text="CPU", font=("Segoe UI", 16, 'bold'), text_color="black")
        self.cpu_label.pack(anchor='w', padx=10, pady=5)

        self.cpu_name_label = ctk.CTkLabel(self, text=f"Name: {cpu_info['cpu_name']}", font=("Segoe UI", 12), text_color="gray")
        self.cpu_name_label.pack(anchor='w', padx=10)

        self.cpu_core_label = ctk.CTkLabel(
            self,
            text=f"Cores: {cpu_info['cores']}, {cpu_info['logical_cores']} logical",
            font=("Segoe UI", 12),
            text_color="gray",
        )
        self.cpu_core_label.pack(anchor='w', padx=10)

        # cpu usage
        self.cpu_usage_text = ctk.StringVar()
        self.cpu_usage_label = ctk.CTkLabel(self, textvariable=self.cpu_usage_text, font=("Segoe UI", 14), text_color="black")
        self.cpu_usage_label.pack(anchor='w', padx=10, pady=5)

        # create theplot
        self.figure = None
        self.ax = None
        self.line = None
        self.fill_area = None
        self.create_plot()

        self.cpu_data = [0] * 60
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(anchor='w', fill='both', expand=True, padx=10, pady=10)

        self.update()

    def create_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("white")
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.ax.set_ylabel("% Utilization", color="gray", fontsize=10)
        self.ax.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
        self.ax.set_xlabel("60 seconds", color="gray", fontsize=10)
        self.ax.set_xticklabels([])
        self.ax.spines['top'].set_color("lightblue")
        self.ax.spines['right'].set_color("lightblue")
        self.ax.spines['bottom'].set_color("lightblue")
        self.ax.spines['left'].set_color("lightblue")
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        self.line, = self.ax.plot([0] * 60, color="#4682B4", linewidth=0.8)
        self.fill_area = self.ax.fill_between(range(60), [0] * 60, color="lightblue")

    def update(self):
        # using psutil for cpu usage
        new_data = psutil.cpu_percent(interval=0)
        self.cpu_usage_text.set(f"{new_data:.1f}%")

        self.cpu_data.append(new_data)
        if len(self.cpu_data) > 60:
            self.cpu_data.pop(0)

        self.line.set_ydata(self.cpu_data)
        self.line.set_xdata(range(len(self.cpu_data)))

        self.fill_area.remove()
        self.fill_area = self.ax.fill_between(range(len(self.cpu_data)), self.cpu_data, color="lightblue", alpha=0.3)

        self.canvas.draw()
        self.after(1000, self.update) # update each second using after. tkinter not thread safe
