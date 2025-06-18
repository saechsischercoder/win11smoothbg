# Win11SmoothBG

**Eliminates tiny, but jarring wallpaper jump between Windows login and desktop - creates buttery smooth transition**

Ever notice how Windows zooms in your wallpaper by approximately 2% when you start typing your password? Well I did... I couldn't stand that jarring transition from the logon screen to desktop, so I built this script to create seamless visual continuity. By intelligently processing and syncing both lock screen and desktop wallpapers, this tool ensures your background flows smoothly from login to desktop.

## ✨ Key Features

### **🎯 Seamless Transition Processing**
- **Smart zoom compensation** - counteracts Windows' 2% zoom behavior
- **Taskbar-aware cropping** - accounts for taskbar height in calculations
- **Centered positioning** - maintains perfect image alignment

### **🖼️ Dual Wallpaper Management**
- **Lock screen synchronization** - sets both lock screen and desktop backgrounds
- **Registry integration** - uses Windows PersonalizationCSP for reliable results
- **Temporary file handling** - processes images in system temp directory

### **🛡️ System Integration**
- **Administrator privilege checking** - ensures proper permissions for registry access
- **DPI scaling awareness** - adapts to different display scaling settings
- **Robust error handling** - graceful failure recovery

## 🚀 Quick Setup

### **Requirements**
- **Python 3.x** with PIL (Pillow) library
- **Administrator privileges** - required for registry modifications

### **Installation**
```bash
pip install pillow
```

## 📖 Usage Examples

### **Basic Usage**
```bash
# Run as Administrator
python win11smoothbg.py "C:\path\to\your\wallpaper.jpg"
```

### **Command Line Help**
```bash
python win11smoothbg.py 
```

**Important:** Always run the script as Administrator. The script will automatically check for admin privileges and prompt you if needed.

## 🔧 How It Works

### **The Problem**
When you start typing your password on Windows login screen, the system applies a subtle ~2% zoom effect to the wallpaper. This creates a noticeable jump when transitioning to the desktop, breaking visual continuity.

### **The Solution**
1. **Processes your wallpaper** - applies compensating zoom and positioning
2. **Sets lock screen image** - uses Windows PersonalizationCSP registry keys
3. **Configures desktop background** - applies tiled wallpaper settings for seamless transition
4. **Stores in temp directory** - keeps processed files organized

### **Technical Details**
- Detects current DPI scaling settings
- Measures actual taskbar height dynamically  
- Applies 2% zoom compensation with centered cropping
- Uses Windows registry APIs for reliable wallpaper setting

## ⚠️ Important Notes

### **Administrator Required**
This script modifies Windows registry keys and requires administrator privileges to function properly. You'll see this error if not running as admin:
```
This script requires administrator privileges. Please run as administrator.
```

### **Supported Formats**
- **Input:** Any image format supported by PIL (JPG, PNG, BMP, etc.)
- **Output:** PNG format stored in system temp directory
- **Processing:** Maintains original aspect ratio with smart cropping

## 🎨 Before & After

**Before:** Tiny, but jarring zoom effect when typing password, noticeable wallpaper jump  
**After:** Buttery smooth transition from login screen to desktop background

## 📋 System Requirements

- **Windows 11** - designed for modern Windows, won't work on Windows 10
