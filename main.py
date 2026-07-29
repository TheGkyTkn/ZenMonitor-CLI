import os
import sys
import time
import psutil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(percent, length=20):
    filled_length = int(length * percent // 100)
    bar = '█' * filled_length + '-' * (length - filled_length)
    return f"[{bar}] {percent:>5.1f}%"

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': cpu_usage,
        'ram_percent': memory.percent,
        'ram_used_gb': memory.used / (1024 ** 3),
        'ram_total_gb': memory.total / (1024 ** 3),
        'disk_percent': disk.percent,
        'disk_used_gb': disk.used / (1024 ** 3),
        'disk_total_gb': disk.total / (1024 ** 3),
    }

def main():
    print("ZenMonitor-CLI Başlatılıyor... (Çıkış için CTRL+C)")
    time.sleep(1)
    
    try:
        while True:
            stats = get_system_stats()
            clear_screen()
            
            print("==================================================")
            print("          ZEN MONITOR - SYSTEM DASHBOARD          ")
            print("==================================================")
            print(f" CPU Kullanımı : {draw_bar(stats['cpu'])}")
            print(f" RAM Kullanımı : {draw_bar(stats['ram_percent'])} ({stats['ram_used_gb']:.1f}/{stats['ram_total_gb']:.1f} GB)")
            print(f" Disk Kullanımı: {draw_bar(stats['disk_percent'])} ({stats['disk_used_gb']:.1f}/{stats['disk_total_gb']:.1f} GB)")
            print("--------------------------------------------------")
            print(" Her 1 saniyede bir güncelleniyor...")
            
    except KeyboardInterrupt:
        print("\n\nZenMonitor kapatıldı. Görüşmek üzere!")
        sys.exit(0)

if __name__ == '__main__':
    main()