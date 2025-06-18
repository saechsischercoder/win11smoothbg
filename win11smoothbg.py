import ctypes
import ctypes.wintypes
import math
import os
import sys
import tempfile
from PIL import Image

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except:
        return False

def set_lock_screen_image(image_path):
    try:
        try:
            import winreg
        except ImportError:
            import _winreg as winreg
        
        abs_path = os.path.abspath(image_path)
        
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP")
        winreg.SetValueEx(key, "LockScreenImagePath", 0, winreg.REG_SZ, abs_path)
        winreg.SetValueEx(key, "LockScreenImageUrl", 0, winreg.REG_SZ, abs_path)
        winreg.SetValueEx(key, "LockScreenImageStatus", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        
        return True
    except:
        return False

def set_desktop_background_tile(image_path):
    try:
        try:
            import winreg
        except ImportError:
            import _winreg as winreg
        
        abs_path = os.path.abspath(image_path)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
        winreg.CloseKey(key)
        
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02
        
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 
            0, 
            abs_path, 
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )
        
        return bool(result)
    except:
        return False

def get_windows_scaling_percent():
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        
        dc = user32.GetDC(0)
        LOGPIXELSX = 88
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
        
        scaling_percent = int((dpi / 96) * 100)
        return scaling_percent
    except:
        return 100

def get_current_taskbar_height():
    try:
        hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
        if not hwnd:
            return 48
        
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        
        height = rect.bottom - rect.top
        width = rect.right - rect.left
        
        if width > height:
            return height
        else:
            return width
    except:
        return 48

def zoom_in_centered_with_taskbar_accounting(image_path):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, 'processed_desktop_background.png')
    
    scaling_percent = get_windows_scaling_percent()
    actual_taskbar_height = get_current_taskbar_height()
    
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    
    taskbar_height_to_remove = actual_taskbar_height
    image_after_taskbar_crop = img.crop((0, 0, orig_w, orig_h - taskbar_height_to_remove))
    
    available_height = orig_h - taskbar_height_to_remove
    new_w = math.ceil(orig_w * 1.02)
    new_h = math.ceil(available_height * 1.02)
    
    zoomed_img = image_after_taskbar_crop.resize((new_w, new_h), Image.LANCZOS)
    
    left = (new_w - orig_w) // 2
    top = (new_h - available_height) // 2
    right = left + orig_w
    bottom = top + available_height
    
    final_img = zoomed_img.crop((left, top, right, bottom))
    final_img.save(output_path)
    
    return output_path

def main_process(input_image_path):
    try:
        set_lock_screen_image(input_image_path)
        processed_image_path = zoom_in_centered_with_taskbar_accounting(input_image_path)
        set_desktop_background_tile(processed_image_path)
        return True
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        print("This script requires administrator privileges. Please run as administrator.")
        sys.exit(1)
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    input_image = sys.argv[1]
    
    if not os.path.exists(input_image):
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    main_process(input_image)
