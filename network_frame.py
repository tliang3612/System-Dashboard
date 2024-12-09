import customtkinter as ctk
import psutil
import platform
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

darker_lightgreen = "#2E8B57"

def get_network_info():
    # Retrieve initial network interface information.
    try:
        net_if_addrs = psutil.net_if_addrs()
        primary_interface = None
        
        wifi_keywords = ['wifi', 'wlan', 'wireless', 'wi-fi', 'wireless lan']
        ethernet_keywords = ['ethernet', 'eth', 'lan', 'local', 'internet']

        interfaces = list(net_if_addrs.keys())
        
        for interface in interfaces:
            interface_lower = interface.lower()
            
            if any(addr.family.name == 'AF_INET' and not addr.address.startswith('127') for addr in net_if_addrs[interface]):
                if any(keyword in interface_lower for keyword in wifi_keywords):
                    primary_interface = interface
                    break
                
        #Fallback if it can't find anything
        if not primary_interface:
            for interface in interfaces:
                interface_lower = interface.lower()
                if any(addr.family.name == 'AF_INET' and not addr.address.startswith('127') for addr in net_if_addrs[interface]):
                    if any(keyword in interface_lower for keyword in ethernet_keywords):
                        primary_interface = interface
                        break

        if not primary_interface:
            for interface in interfaces:
                if any(addr.family.name == 'AF_INET' and not addr.address.startswith('127') for addr in net_if_addrs[interface]):
                    primary_interface = interface
                    break
        
        return {
            "primary_interface": primary_interface or "Unknown",
            "initial_io": psutil.net_io_counters(pernic=True).get(primary_interface, None)
        }
    except Exception as e:
        return {
            "primary_interface": f"Error detecting interface: {str(e)}",
            "initial_io": None
        }

class NetworkFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        self.grid_columnconfigure(0, weight=3)  # col 0 for network info
        self.grid_columnconfigure(1, weight=0)  # col 1 for slider
        self.grid_rowconfigure(4, weight=1)  # row 4 for graph

        network_info = get_network_info()
        self.network_interface = network_info['primary_interface']
        self.initial_network_io = network_info['initial_io']
        
        self.upload_data = [0] * 3600
        self.download_data = [0] * 3600
        
        self.create_network_labels(network_info)
        self.create_plot()
        self.create_slider()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.last_network_io = self.initial_network_io
        self.time_range = 60
        self.update()

    def create_network_labels(self, network_info):
        self.network_label = ctk.CTkLabel(
            self,
            text="Network Usage Monitor",
            font=("Segoe UI", 18, "bold"),
            text_color="darkgreen",
        )
        self.network_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.upload_text = ctk.StringVar(value="Upload: 0 Mbps")
        self.download_text = ctk.StringVar(value="Download: 0 Mbps")
        
        self.upload_label = ctk.CTkLabel(
            self,
            textvariable=self.upload_text,
            font=("Segoe UI", 16, "italic"),
            text_color="green",
        )
        self.upload_label.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

        self.download_label = ctk.CTkLabel(
            self,
            textvariable=self.download_text,
            font=("Segoe UI", 16, "italic"),
            text_color="blue",
        )
        self.download_label.grid(row=2, column=0, sticky="nw", padx=10, pady=5)

        self.interface_label = ctk.CTkLabel(
            self,
            text=f"Interface: {self.network_interface}",
            font=("Segoe UI", 13, "normal"),
            text_color="gray",
        )
        self.interface_label.grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.time_range = 60

    def create_plot(self):
        self.figure = Figure(figsize=(7, 2), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("white")
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.set_yticks([0, 20, 40, 60, 80, 100])
        self.ax.set_ylabel("Mbps", color="gray", fontsize=10)
        self.ax.set_xticklabels([])

        step = max(1, self.time_range // 20)
        ticks = list(range(0, self.time_range + 1, step))
        self.ax.set_xticks(ticks)

        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)
        
        for spine in ['top', 'right', 'bottom', 'left']:
            self.ax.spines[spine].set_color(darker_lightgreen)
        
        self.ax.grid(color="lightgreen", linestyle="-", linewidth=0.3, alpha=0.7)

        self.upload_line, = self.ax.plot([0] * 60, color="green", linewidth=0.8, label="Upload")
        self.download_line, = self.ax.plot([0] * 60, color="blue", linewidth=0.8, label="Download")
        
        self.ax.legend(loc='upper right', fontsize=8)

    def create_slider(self):
        slider_frame = ctk.CTkFrame(self, fg_color="transparent")
        slider_frame.grid(row=0, column=1, rowspan=2, sticky="ne", padx=10, pady=5)

        slider_label = ctk.CTkLabel(slider_frame, text="Select Time Range (minutes):", text_color="black")
        slider_label.pack(anchor="e", pady=5)

        min_label = ctk.CTkLabel(slider_frame, text="1", text_color="gray")
        min_label.pack(side="left", padx=5)

        self.time_slider = ctk.CTkSlider(
            slider_frame, from_=60, to=3600, number_of_steps=400, command=self.update_time_range
        )
        self.time_slider.set(60)  # Default to 60 seconds (1 minute)
        self.time_slider.pack(side="left", padx=5)

        max_label = ctk.CTkLabel(slider_frame, text="60", text_color="gray")
        max_label.pack(side="right", padx=5)

    def update_time_range(self, value):
        self.time_range = int(float(value))
        self.update_plot()

    def update(self):
        try:
            current_network_io = psutil.net_io_counters(pernic=True).get(self.network_interface)
            
            if current_network_io and self.last_network_io:
                download_bytes = current_network_io.bytes_recv - self.last_network_io.bytes_recv
                upload_bytes = current_network_io.bytes_sent - self.last_network_io.bytes_sent
                
                download_mbps = (download_bytes * 8) / (1024 * 1024)
                upload_mbps = (upload_bytes * 8) / (1024 * 1024)

                self.download_text.set(f"Download: {download_mbps:.2f} Mbps")
                self.upload_text.set(f"Upload: {upload_mbps:.2f} Mbps")

                self.download_data.append(download_mbps)
                self.upload_data.append(upload_mbps)

                self.download_data = self.download_data[-3600:]
                self.upload_data = self.upload_data[-3600:]

                self.last_network_io = current_network_io

                self.update_plot()

        except Exception as e:
            print(f"Network update error: {e}")

        self.after(1000, self.update)

    def update_plot(self):
        download_to_plot = self.download_data[-self.time_range:]
        upload_to_plot = self.upload_data[-self.time_range:]

        self.download_line.set_ydata(download_to_plot)
        self.download_line.set_xdata(range(len(download_to_plot)))
        
        self.upload_line.set_ydata(upload_to_plot)
        self.upload_line.set_xdata(range(len(upload_to_plot)))

        self.ax.set_xlim(0, self.time_range)
        self.ax.set_xlabel(f"Last {self.time_range//60} minute(s)", color="gray", fontsize=10)

        step = max(1, self.time_range // 20)
        ticks = list(range(0, self.time_range + 1, step))
        self.ax.set_xticks(ticks)

        self.canvas.draw()
