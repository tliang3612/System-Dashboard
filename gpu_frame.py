import customtkinter as ctk
import GPUtil
import subprocess

darker_lightblue = "#468284"

def get_gpu_info():
    gpus = GPUtil.getGPUs()

    if len(gpus) > 0:
        gpu_info = {
            "gpu_name": gpus[0].name,
            "memory_total": gpus[0].memoryTotal,
            "memory_free": gpus[0].memoryFree,
            "memory_used": gpus[0].memoryUsed,
            "gpu_temperature": gpus[0].temperature,
        }
        return gpu_info
    else:
        print("Checking for other systems.")


class GPUFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        self.gpu_name_label = ctk.CTkLabel(self, text="GPU: ", font=("Segoe UI", 16))
        self.gpu_name_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.gpu_usage_label = ctk.CTkLabel(self, text="GPU Usage: 0%", font=("Segoe UI", 16, "italic"))
        self.gpu_usage_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.update_gpu_info()

    def update_gpu_info(self):
        gpu_info = get_gpu_info() 
        
        self.gpu_name_label.configure(text=f"GPU: {gpu_info['gpu_name']}")
        self.gpu_usage_label.configure(text=f"GPU Temperature: {gpu_info['gpu_temperature']}°C")
        
        self.after(1000, self.update_gpu_info)
        


