import customtkinter as ctk
import psutil
import platform
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


darker_lightblue = "#4682B4"

def get_cpu_info():
    # determine cpu name by going into
    cpu_name = None
    if platform.system() == "Windows":
        from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
        try:
            registry_key = OpenKey(HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") #get reference to first cpu registry key location
            cpu_name, reg = QueryValueEx(registry_key, "ProcessorNameString") #retrieve value of ProcessorNameString from the key to get the cpu name
        except Exception as e:
            cpu_name = "Unknown CPU"
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_name = line.split(":")[1].strip()
                        break
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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # toggle cpu frame info
        self.is_collapsed = False
        self.toggle_button = ctk.CTkButton(
            self,
            text="Hide CPU Frame",
            command=self.toggle_cpu_frame,
            width=100,
            fg_color="blue",
            text_color="white",
        )
        self.toggle_button.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

        #contains the container for cpu frame contents
        self.contents_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.contents_frame.grid_columnconfigure(0, weight=1)
        self.contents_frame.grid_columnconfigure(1, weight=0)
        self.contents_frame.grid_rowconfigure(5, weight=1)
        self.contents_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")


        # get info about the cpu
        cpu_info = get_cpu_info()
        self.cpu_usage_text = None
        self.cpu_label = None
        self.cpu_usage_label = None
        self.cpu_name_label = None
        self.cpu_core_label = None
        self.create_cpu_labels(cpu_info)

        # cpu usage
        self.time_range = 60
        self.cpu_usage_data = [0] * 3600

        # create theplot
        self.figure = None
        self.ax = None
        self.line = None
        self.fill_area = None
        self.create_plot()

        #create the timeline slider
        self.time_slider = None
        self.create_slider()

        self.canvas = FigureCanvasTkAgg(self.figure, self.contents_frame)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2,  sticky="nsew", padx=10, pady=10)

        self.update()

    def create_cpu_labels(self, cpu_info):
        # title label
        self.cpu_label = ctk.CTkLabel(
            self.contents_frame,
            text="CPU Usage Monitor",
            font=("Segoe UI", 18, "bold"),
            text_color="darkblue",
        )

        # cpu usage label
        self.cpu_usage_text = ctk.StringVar()
        self.cpu_usage_label = ctk.CTkLabel(
            self.contents_frame,
            textvariable=self.cpu_usage_text,
            font=("Segoe UI", 16, "italic"),
            text_color="black",
        )

        # cpu name label
        self.cpu_name_label = ctk.CTkLabel(
            self.contents_frame,
            text=f"{cpu_info['cpu_name']}",
            font=("Segoe UI", 13, "normal"),
            text_color="blue",
        )

        # cpu core count label
        self.cpu_core_label = ctk.CTkLabel(
            self.contents_frame,
            text=f"Cores: {cpu_info['cores']}, {cpu_info['logical_cores']} logical",
            font=("Segoe UI", 13, "italic"),
            text_color="gray",
        )

        self.cpu_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.cpu_usage_label.grid(row=1, column=0, columnspan = 1, sticky="nw", padx=10, pady=5)
        self.cpu_name_label.grid(row=2, column=0, columnspan = 2,sticky="nw", padx=10, pady=5)
        self.cpu_core_label.grid(row=3, column=0, columnspan = 2,sticky="nw", padx=10, pady=5)

    def create_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        # init the axes
        self.ax.set_facecolor("white")
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.ax.set_ylabel("% Utilization", color="gray", fontsize=10)
        self.ax.set_xticklabels([])

        step = max(1, self.time_range // 20)  # divide time range into 20 steps
        ticks = list(range(0, self.time_range + 1, step)) # create array of steps
        self.ax.set_xticks(ticks)

        # update the x label based on time range
        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)
        self.ax.spines['top'].set_color(darker_lightblue)
        self.ax.spines['right'].set_color(darker_lightblue)
        self.ax.spines['bottom'].set_color(darker_lightblue)
        self.ax.spines['left'].set_color(darker_lightblue)
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        # init the line and fill
        self.line, = self.ax.plot([0] * 60, color=darker_lightblue, linewidth=0.8)
        self.fill_area = self.ax.fill_between(range(self.time_range), [0] * self.time_range, color="lightblue", alpha=0.3)

    def create_slider(self):
        # slider frame
        slider_frame = ctk.CTkFrame(self.contents_frame, fg_color="transparent")
        slider_frame.grid(row=0, column=1, rowspan=2, sticky="ne", padx=10, pady=5)

        # slider label
        slider_label = ctk.CTkLabel(slider_frame, text="Select Time Range (minutes):", text_color="black")
        slider_label.pack(anchor="e", pady=5)

        # 1 min label
        min_label = ctk.CTkLabel(slider_frame, text="1", text_color="gray")
        min_label.pack(side="left", padx=5)

        # init the slider
        self.time_slider = ctk.CTkSlider(
            slider_frame, from_=60, to=3600, number_of_steps=60, command=self.update_time_range
        )
        self.time_slider.set(60)
        self.time_slider.pack(side="left", padx=5)

        # 60 mins label
        max_label = ctk.CTkLabel(slider_frame, text="60", text_color="gray")
        max_label.pack(side="right", padx=5)

    # command for slider increments
    def update_time_range(self, value):
        self.time_range = int(float(value))
        self.update_plot()

    def update(self):
        # using psutil for cpu usage
        self.update_cpu_info()
        self.update_plot()
        self.after(1000, self.update) # update each second using after. tkinter not thread safe

    def update_cpu_info(self):
        new_data = psutil.cpu_percent(interval=0)
        self.cpu_usage_text.set(f"CPU Usage: {new_data:.1f}%")

        self.cpu_usage_data.append(new_data)
        if len(self.cpu_usage_data) > 60:
            self.cpu_usage_data.pop(0)

    def update_plot(self):
        data_to_plot = self.cpu_usage_data[-self.time_range:]

        # update the line and fill area
        self.line.set_ydata(data_to_plot)
        self.line.set_xdata(range(len(data_to_plot)))
        if self.fill_area:
            self.fill_area.remove()
        self.fill_area = self.ax.fill_between(range(len(data_to_plot)), data_to_plot, color="lightblue", alpha=0.3)

        # update xlim
        self.ax.set_xlim(0, self.time_range)

        #update xlabel
        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)

        #update xticks
        step = max(1, self.time_range // 20)
        ticks = list(range(0, self.time_range + 1, step))
        self.ax.set_xticks(ticks)

        self.canvas.draw()

    def toggle_cpu_frame(self):
        if self.is_collapsed:
            self.contents_frame.grid()
            self.configure(fg_color="white")
            self.toggle_button.configure(text="Hide CPU Frame")
        else:
            self.contents_frame.grid_remove()
            self.configure(fg_color="transparent")
            self.toggle_button.configure(text="Show CPU Frame")

        self.is_collapsed = not self.is_collapsed
