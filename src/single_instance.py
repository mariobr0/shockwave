import ctypes
import sys

# Windows constants
ERROR_ALREADY_EXISTS = 183

_mutex_handle = None

def check_single_instance(mutex_name="Local\\Shockwave_App_Mutex_v092"):
    """
    Ensures only one instance of Shockwave runs at any given time
    using a native Windows Named Mutex.
    
    Returns:
        bool: True if this is the only running instance, False if a duplicate was detected.
    """
    global _mutex_handle
    
    try:
        kernel32 = ctypes.windll.kernel32
        # Create or open named mutex
        _mutex_handle = kernel32.CreateMutexW(None, False, mutex_name)
        last_error = kernel32.GetLastError()
        
        if last_error == ERROR_ALREADY_EXISTS:
            return False
        return True
    except Exception as e:
        print(f"Single instance mutex notice: {e}")
        return True

def release_single_instance():
    """Releases the mutex handle upon application termination."""
    global _mutex_handle
    if _mutex_handle:
        try:
            ctypes.windll.kernel32.CloseHandle(_mutex_handle)
        except Exception:
            pass
        _mutex_handle = None
