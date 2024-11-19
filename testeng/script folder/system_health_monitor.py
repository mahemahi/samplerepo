import psutil
import time
import logging

# Configure logging
logging.basicConfig(filename='system_health.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

def check_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"High CPU usage: {cpu_usage}%")

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        logging.warning(f"High memory usage: {memory.percent}%")

def check_disk():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        logging.warning(f"High disk usage: {disk.percent}%")

def check_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if proc.info['cpu_percent'] > CPU_THRESHOLD:
            logging.warning(f"High CPU process: {proc.info['name']} (PID: {proc.info['pid']}) - {proc.info['cpu_percent']}%")

def main():
    while True:
        check_cpu()
        check_memory()
        check_disk()
        check_processes()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()