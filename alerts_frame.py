import customtkinter as ctk
from plyer import notification
import time


class AlertsFrame(ctk.CTkFrame):
    def __init__(self, parent, cpu_frame, gpu_frame, memory_frame):
        super().__init__(parent, fg_color="white")

        self.cpu_frame = cpu_frame
        self.gpu_frame = gpu_frame
        self.memory_frame = memory_frame

        self.last_alert_time_dict = {"cpu": 0, "gpu" : 0, "memory":0}
        self.threshold_dict = {"cpu": 100, "gpu" : 100, "memory": 100}

        self.grid_columnconfigure(0, weight=0)

        self.instruction_label = ctk.CTkLabel(
            self,
            text="Set System Alerts for Usage",
            font=("Segoe UI", 16, "bold"),
            text_color="black",
        )
        self.instruction_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.cpu_threshold_entry = ctk.CTkEntry(self, placeholder_text="Enter CPU Usage threshold")
        self.cpu_threshold_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.gpu_threshold_entry = ctk.CTkEntry(self, placeholder_text="Enter GPU Usage threshold")
        self.gpu_threshold_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.memory_threshold_entry = ctk.CTkEntry(self, placeholder_text="Enter MEMORY Usage threshold")
        self.memory_threshold_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.save_button = ctk.CTkButton(
            self,
            text="Set Threshold",
            command=self.save_thresholds,
            fg_color="blue",
            text_color="white",
        )
        self.save_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.cpu_status_label = ctk.CTkLabel(
            self,
            text="No CPU threshold set.",
            font=("Segoe UI", 12),
            text_color="gray",
        )

        self.gpu_status_label = ctk.CTkLabel(
            self,
            text="No GPU threshold set.",
            font=("Segoe UI", 12),
            text_color="gray",
        )

        self.memory_status_label = ctk.CTkLabel(
            self,
            text="No MEMORY threshold set.",
            font=("Segoe UI", 12),
            text_color="gray",
        )

        self.cpu_status_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.gpu_status_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.memory_status_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.monitor()

    def save_thresholds(self):
        try:
            cpu_threshold = self.cpu_threshold_entry.get()
            if cpu_threshold.strip():
                self.threshold_dict["cpu"] = float(cpu_threshold)
                self.cpu_status_label.configure(
                    text=f"CPU Alert threshold set to {self.threshold_dict['cpu']}%.",
                    text_color="green",
                )

            gpu_threshold = self.gpu_threshold_entry.get()
            if gpu_threshold.strip():
                self.threshold_dict["gpu"] = float(gpu_threshold)
                self.gpu_status_label.configure(
                    text=f"GPU Alert threshold set to {self.threshold_dict['gpu']}%.",
                    text_color="green",
                )

            memory_threshold = self.memory_threshold_entry.get()
            if memory_threshold.strip():
                self.threshold_dict["memory"] = float(memory_threshold)
                self.memory_status_label.configure(
                    text=f"MEMORY Alert threshold set to {self.threshold_dict['memory']}%.",
                    text_color="green",
                )

        except ValueError:
            pass

    def monitor(self):
        if self.threshold_dict["cpu"] is not None:
            try:
                usage = self.cpu_frame.cpu_usage_data[-1]
                if usage > self.threshold_dict["cpu"]:
                    self.check_and_send_alert(usage, "cpu")
            except (ValueError, IndexError):
                pass

        if self.threshold_dict["gpu"] is not None:
            try:
                current_usage = self.gpu_frame.gpu_usage_data[-1]
                usage = current_usage
                if usage > self.threshold_dict["gpu"]:
                    self.check_and_send_alert(usage, "gpu")
            except (ValueError, IndexError):
                pass

        if self.threshold_dict["memory"] is not None:
            try:
                current_usage = self.memory_frame.memory_data[-1]
                if current_usage > self.threshold_dict["memory"]:
                    self.check_and_send_alert(current_usage, "memory")
            except (ValueError, IndexError):
                pass

        self.after(1000, self.monitor)

    def check_and_send_alert(self, usage, type):
        current_time = time.time()
        if current_time - self.last_alert_time_dict[type] >= 10:
            self.send_alert(usage, type)
            self.last_alert_time_dict[type] = current_time

    def send_alert(self, usage, type):
        notification.notify(
            title="CPU Alert",
            message=f"{type.upper()} usage is at {usage:.1f}%, exceeding the threshold!",
            app_name="PC Dashboard",
        )
