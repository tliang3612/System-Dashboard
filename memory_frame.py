import customtkinter as ctk
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

darker_lightblue = "#4682B4"

class MemoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        self.grid_columnconfigure(0, weight=3)  # col 0 for memory info
        self.grid_columnconfigure(1, weight=0)  # col 1 for slider
        self.grid_rowconfigure(4, weight=1)  # row 4 for graph

        self.memory_usage_text = None
        self.memory_label = None
        self.memory_usage_label = None
        self.memory_stats_label = None
        self.create_memory_labels()

        self.time_range = 60
        self.memory_data = [0] * 3600

        self.figure = None
        self.ax = None
        self.line = None
        self.fill_area = None
        self.create_plot()

        self.time_slider = None
        self.create_slider()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.update()

    def create_memory_labels(self):
        self.memory_label = ctk.CTkLabel(
            self,
            text="Memory Usage Monitor",
            font=("Segoe UI", 18, "bold"),
            text_color="darkblue",
        )
        self.memory_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.memory_usage_text = ctk.StringVar()
        self.memory_usage_label = ctk.CTkLabel(
            self,
            textvariable=self.memory_usage_text,
            font=("Segoe UI", 16, "italic"),
            text_color="black",
        )
        self.memory_usage_label.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024 ** 3)  # Convert to GB
        self.memory_stats_label = ctk.CTkLabel(
            self,
            text=f"Total Memory: {total_memory:.2f} GB",
            font=("Segoe UI", 13, "normal"),
            text_color="gray",
        )
        self.memory_stats_label.grid(row=2, column=0, sticky="nw", padx=10, pady=5)

    def create_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("white")
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks([0, 20, 40, 60, 80, 100])
        self.ax.set_ylabel("% Memory Usage", color="gray", fontsize=10)
        self.ax.set_xticklabels([])

        step = max(1, self.time_range // 20)
        ticks = list(range(0, self.time_range + 1, step))
        self.ax.set_xticks(ticks)

        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)
        self.ax.spines['top'].set_color(darker_lightblue)
        self.ax.spines['right'].set_color(darker_lightblue)
        self.ax.spines['bottom'].set_color(darker_lightblue)
        self.ax.spines['left'].set_color(darker_lightblue)
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        self.line, = self.ax.plot([0] * 60, color=darker_lightblue, linewidth=0.8)
        self.fill_area = self.ax.fill_between(range(self.time_range), [0] * self.time_range, color="lightblue", alpha=0.3)

    def create_slider(self):
        # Slider frame
        slider_frame = ctk.CTkFrame(self, fg_color="transparent")
        slider_frame.grid(row=0, column=1, rowspan=2, sticky="ne", padx=10, pady=5)

        # Slider label
        slider_label = ctk.CTkLabel(slider_frame, text="Select Time Range (minutes):", text_color="black")
        slider_label.pack(anchor="e", pady=5)

        # 1 min label
        min_label = ctk.CTkLabel(slider_frame, text="1", text_color="gray")
        min_label.pack(side="left", padx=5)

        # Init the slider
        self.time_slider = ctk.CTkSlider(
            slider_frame, from_=60, to=3600, number_of_steps=400, command=self.update_time_range
        )
        self.time_slider.set(60)  # Default to 60 seconds (1 minute)
        self.time_slider.pack(side="left", padx=5)

        # 60 mins label
        max_label = ctk.CTkLabel(slider_frame, text="60", text_color="gray")
        max_label.pack(side="right", padx=5)

    def update_time_range(self, value):
        self.time_range = int(float(value))
        self.update_plot()

    def update(self):
        memory = psutil.virtual_memory()
        memory_usage_percent = memory.percent
        self.memory_usage_text.set(f"{memory_usage_percent:.1f}%")

        self.memory_data.append(memory_usage_percent)
        if len(self.memory_data) > 3600:
            self.memory_data.pop(0)

        self.update_plot()
        self.after(1000, self.update)  # Update each second

    def update_plot(self):
        data_to_plot = self.memory_data[-self.time_range:]

        self.line.set_ydata(data_to_plot)
        self.line.set_xdata(range(len(data_to_plot)))
        if self.fill_area:
            self.fill_area.remove()
        self.fill_area = self.ax.fill_between(range(len(data_to_plot)), data_to_plot, color="lightblue", alpha=0.3)

        self.ax.set_xlim(0, self.time_range)

        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)

        step = max(1, self.time_range // 20)
        ticks = list(range(0, self.time_range + 1, step))
        self.ax.set_xticks(ticks)

        self.canvas.draw()
