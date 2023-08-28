import psutil
import subprocess
import sys

def get_ram_usage():
    return psutil.virtual_memory().used / (1024 ** 3)  # Convert bytes to gigabytes

def send_notification(message):
    # Use subprocess to call a command-line notification tool (change "notify-send" to your preferred tool)
    subprocess.run(["notify-send", "Alert", message])

def main(args):
    threshold_gb = 5.30
    while True:
        ram_usage_gb = get_ram_usage()
        if ram_usage_gb > threshold_gb:
            message = f"Alerta: Uso de RAM superó los {threshold_gb:.2f} GB ({ram_usage_gb:.2f} GB)"
            send_notification(message)
        print(f"Uso actual de RAM: {ram_usage_gb:.2f} GB")
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
