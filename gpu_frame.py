import customtkinter as ctk
import psutil
import platform
import os
import GPUtil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
        return {
            "gpu_name": "Unknown GPU",
            "memory_total": "N/A",
            "memory_free": "N/A",
            "memory_used": "N/A",
            "gpu_temperature": "N/A",
        }

