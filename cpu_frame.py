import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class CPUFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(self, text="CPU", font=("Segoe UI", 16, 'bold'), bg="white").pack(anchor='w')
        tk.Label(self, text="CPU name here", font=("Segoe UI", 12), bg="white").pack(anchor='w')

        self.cpu_usage_text = tk.StringVar()

        self.figure = None
        self.ax = None
        self.line = None
        self.fill_area = None
        self.create_plot()

        self.cpu_data = [0] * 60

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(anchor='w', fill='both', expand=True)

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
        self.ax.set_xlabel("60 seconds", color="gray", fontsize=10)
        self.ax.set_xticklabels([])
        self.ax.spines['top'].set_color("#4682B4")
        self.ax.spines['right'].set_color("#4682B4")
        self.ax.spines['bottom'].set_color("#4682B4")
        self.ax.spines['left'].set_color("#4682B4")
        self.ax.grid(color="lightblue", linestyle="-", linewidth=0.3, alpha=0.7)

        self.line, = self.ax.plot([0] * 60, color="#4682B4", linewidth=0.8)
        self.fill_area = self.ax.fill_between(range(60), [0] * 60, color="#4682B4", alpha=0.3)

    def update(self):
        new_data = random.randint(0, 100)
        self.cpu_usage_text.set(f"{new_data}%")

        self.cpu_data.append(new_data)
        if len(self.cpu_data) > 60:
            self.cpu_data.pop(0)

        self.line.set_ydata(self.cpu_data)
        self.line.set_xdata(range(len(self.cpu_data)))

        self.fill_area.remove()
        self.fill_area = self.ax.fill_between(range(len(self.cpu_data)), self.cpu_data, color="#4682B4", alpha=0.3)

        self.canvas.draw()
        self.after(1000, self.update) #basically thread but for tkinter



