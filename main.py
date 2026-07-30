import os
import sys
import time
import ctypes
from datetime import datetime
import psutil


if os.name == 'nt':
    import msvcrt
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

try:
    from plyer import notification
    HAS_NOTIFICATION = True
except ImportError:
    HAS_NOTIFICATION = False

LAST_NOTIF_TIME = 0
IS_MINI_MODE = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(percent, length=15):
    filled_length = int(length * percent // 100)
    bar = '█' * filled_length + '-' * (length - filled_length)
    return f"[{bar}] {percent:>5.1f}%"

def set_window_hud_mode(enable=True):
    if os.name != 'nt':
        return

    hwnd = kernel32.GetConsoleWindow()
    if not hwnd:
        return

    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)

    if enable:
        os.system("mode con: cols=45 lines=10")
        time.sleep(0.05)
        
        rect = (ctypes.c_long * 4)()
        user32.GetWindowRect(hwnd, rect)
        win_w = rect[2] - rect[0]
        win_h = rect[3] - rect[1]

        x = screen_w - win_w - 15
        y = screen_h - win_h - 45

        user32.MoveWindow(hwnd, x, y, win_w, win_h, True)
        user32.SetWindowPos(hwnd, -1, x, y, win_w, win_h, 0x0040)
    else:
        os.system("mode con: cols=60 lines=20")
        time.sleep(0.05)
        
        rect = (ctypes.c_long * 4)()
        user32.GetWindowRect(hwnd, rect)
        win_w = rect[2] - rect[0]
        win_h = rect[3] - rect[1]

        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2

        user32.MoveWindow(hwnd, x, y, win_w, win_h, True)
        user32.SetWindowPos(hwnd, -2, x, y, win_w, win_h, 0x0040)

def send_windows_notification(title, message):
    global LAST_NOTIF_TIME
    if HAS_NOTIFICATION and (time.time() - LAST_NOTIF_TIME > 60):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="ZenMonitor",
                timeout=5
            )
            LAST_NOTIF_TIME = time.time()
        except Exception:
            pass

def get_top_io_processes(limit=2):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
        try:
            io = proc.info['io_counters']
            if io:
                total_bytes = io.read_bytes + io.write_bytes
                processes.append({
                    'name': proc.info['name'],
                    'io_mb': total_bytes / (1024 ** 2)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(processes, key=lambda x: x['io_mb'], reverse=True)[:limit]

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    if memory.percent > 85:
        send_windows_notification("⚠️ Yüksek RAM!", f"RAM %{memory.percent:.1f} doldu.")
    if disk.percent > 90:
        send_windows_notification("🚨 Disk Dolu!", f"C: %{disk.percent:.1f} dolu.")

    top_io = get_top_io_processes(2)

    return {
        'cpu': cpu_usage,
        'ram_percent': memory.percent,
        'ram_used_gb': memory.used / (1024 ** 3),
        'ram_total_gb': memory.total / (1024 ** 3),
        'disk_percent': disk.percent,
        'disk_used_gb': disk.used / (1024 ** 3),
        'disk_total_gb': disk.total / (1024 ** 3),
        'top_io': top_io
    }

def check_toggle_key():
    global IS_MINI_MODE
    if os.name == 'nt' and msvcrt.kbhit():
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            sub_key = msvcrt.getch()
            if sub_key == b'B':  # F8 Scan Code
                IS_MINI_MODE = not IS_MINI_MODE
                set_window_hud_mode(IS_MINI_MODE)

def main():
    print("ZenMonitor-CLI Başlatılıyor... (Çıkış için CTRL+C)")
    time.sleep(1)
    
    try:
        while True:
            check_toggle_key()

            if IS_MINI_MODE and os.name == 'nt':
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010)

            stats = get_system_stats()
            clear_screen()
            
            if IS_MINI_MODE:
                print(" ── ZEN MONITOR [MINI HUD] ── (F8: Büyüt)")
                print(f" CPU : {draw_bar(stats['cpu'], 12)}")
                print(f" RAM : {draw_bar(stats['ram_percent'], 12)} ({stats['ram_used_gb']:.1f}/{stats['ram_total_gb']:.1f}G)")
                print(f" DSK : {draw_bar(stats['disk_percent'], 12)} ({stats['disk_used_gb']:.1f}/{stats['disk_total_gb']:.1f}G)")
                print(" ─────────────────────────────────────────")
                for proc in stats['top_io']:
                    p_name = (proc['name'][:12] + '..') if len(proc['name']) > 14 else proc['name']
                    print(f"  • {p_name:<14} -> {proc['io_mb']:.1f} MB")
            else:
                print("==================================================")
                print("          ZEN MONITOR - SYSTEM DASHBOARD          ")
                print("==================================================")
                print(f" CPU Kullanımı : {draw_bar(stats['cpu'])}")
                print(f" RAM Kullanımı : {draw_bar(stats['ram_percent'])} ({stats['ram_used_gb']:.1f}/{stats['ram_total_gb']:.1f} GB)")
                print(f" Disk Kullanımı: {draw_bar(stats['disk_percent'])} ({stats['disk_used_gb']:.1f}/{stats['disk_total_gb']:.1f} GB)")
                print("--------------------------------------------------")
                print("  DISK & I/O CONTROL")
                for proc in stats['top_io']:
                    p_name = (proc['name'][:18] + '..') if len(proc['name']) > 20 else proc['name']
                    print(f"  • {p_name:<20} -> İşlenen: {proc['io_mb']:.1f} MB")
                print("--------------------------------------------------")
                print("  [F8] Tuşuna Basarak Sağ Alt HUD Moduna Geç!")

    except KeyboardInterrupt:
        set_window_hud_mode(False)
        print("\n\nZenMonitor kapatıldı. Görüşmek üzere!")
        sys.exit(0)

if __name__ == '__main__':
    main()
