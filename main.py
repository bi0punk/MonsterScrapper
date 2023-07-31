#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py
#  
#  Copyright 2023  <sysbot@kali>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

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
