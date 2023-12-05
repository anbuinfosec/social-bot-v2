import os
import asyncio
import speedtest
import psutil
import platform
import os
import time

def print_app_info():
  print(f" * VERSION: 1.0.1")
  print(f" * AUTHOR: anbuinfosec")
  print(f" * EMAIL: anbuinfosec@gmail.com")


def clear():
  """
  A function for clear your terminal
  """
  os.system("clear")



def convert_bytes(num):
    """
    Convert bytes to a human-readable format.
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get_system_info():
  """
  Gettin system info
  """
  line = '___________________________'
  ram = psutil.virtual_memory()
  storage = psutil.disk_usage('/')
  uptime_seconds = time.time() - psutil.boot_time()
  uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
  uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
  uptime_days, uptime_hours = divmod(uptime_hours, 24)
  cpu = psutil.cpu_percent(interval=1)
  return f"▣ Total RAM: {convert_bytes(ram.total)}\n▣ Available RAM: {convert_bytes(ram.available)}\n▣ Used RAM: {convert_bytes(ram.used)}\n{line}\n▣ Total Storage: {convert_bytes(storage.total)}\n▣ Used Storage: {convert_bytes(storage.used)}\n▣ Free Storage: {convert_bytes(storage.free)}\n{line}\n▣ System Uptime: {int(uptime_days)} days, {int(uptime_hours)} hours, {int(uptime_minutes)} minutes\n▣ CPU Usage: {cpu}%\n{line}\nUninstall Telegram and enjoy your life!"
