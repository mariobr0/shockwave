import ctypes
import ctypes.wintypes
import threading
import time

# Win32 Constants
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312

VK_MAP = {
    "f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
    "f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
    "f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
    "space": 0x20, "tab": 0x09, "esc": 0x1B, "escape": 0x1B,
    "enter": 0x0D, "return": 0x0D, "backspace": 0x08,
    "pause": 0x13, "capslock": 0x14, "insert": 0x2D,
    "delete": 0x2E, "home": 0x24, "end": 0x23,
    "pageup": 0x21, "pagedown": 0x22
}

def parse_hotkey_string(hotkey_str):
    parts = [p.strip().lower() for p in hotkey_str.split("+") if p.strip()]
    modifiers = MOD_NOREPEAT
    vk = 0
    
    for part in parts:
        if part in ["ctrl", "control"]:
            modifiers |= MOD_CONTROL
        elif part == "alt":
            modifiers |= MOD_ALT
        elif part == "shift":
            modifiers |= MOD_SHIFT
        elif part in ["win", "windows", "super"]:
            modifiers |= MOD_WIN
        elif part in VK_MAP:
            vk = VK_MAP[part]
        elif len(part) == 1:
            vk = ord(part.upper())
            
    return modifiers, vk

class SystemHotkeyManager:
    def __init__(self, hotkey_str, callback):
        self.hotkey_str = hotkey_str
        self.callback = callback
        self.thread_id = None
        self.running = False
        self.hotkey_id = 1001
        self._thread = None
        
        self.start()

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._msg_loop, daemon=True)
        self._thread.start()

    def _msg_loop(self):
        self.thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        user32 = ctypes.windll.user32
        
        modifiers, vk = parse_hotkey_string(self.hotkey_str)
        if vk == 0:
            vk = 0x7B  # Default F12
            
        success = user32.RegisterHotKey(None, self.hotkey_id, modifiers, vk)
        if not success:
            # Try without MOD_NOREPEAT (for older Windows versions)
            modifiers &= ~MOD_NOREPEAT
            success = user32.RegisterHotKey(None, self.hotkey_id, modifiers, vk)
            
        if success:
            print(f"[System Hotkey] Registered global key '{self.hotkey_str.upper()}' via Win32 RegisterHotKey.")
        else:
            print(f"[System Hotkey] Warning: Failed to register '{self.hotkey_str.upper()}'. Key might be locked by another app.")

        msg = ctypes.wintypes.MSG()
        while self.running:
            # PeekMessage allows graceful thread exit
            res = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if res <= 0:
                break
                
            if msg.message == WM_HOTKEY and msg.wParam == self.hotkey_id:
                if self.callback:
                    try:
                        self.callback()
                    except Exception as e:
                        print(f"Hotkey callback error: {e}")
                        
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        user32.UnregisterHotKey(None, self.hotkey_id)

    def stop(self):
        self.running = False
        if self.thread_id:
            ctypes.windll.user32.PostThreadMessageW(self.thread_id, 0x0012, 0, 0)  # WM_QUIT
