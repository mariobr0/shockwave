import tkinter as tk
import queue
import os
import sys
import winsound
import ctypes

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    candidate = os.path.join(root_path, relative_path)
    if os.path.exists(candidate):
        return candidate
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def play_ready_sound():
    sound_path = get_resource_path(os.path.join("alert", "ready.wav"))
    if os.path.exists(sound_path):
        try:
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Audio playback error: {e}")

class WinVoiceUI:
    def __init__(self, message_queue, position="bottom-left"):
        self.queue = message_queue
        self.root = tk.Tk()
        
        # Hide window immediately during setup to avoid top-left blank flash
        self.root.withdraw()
        
        # Set window icon
        icon_path = get_resource_path(os.path.join("icons", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass
                
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#2d2d2d")
        
        # --- Left Grip / Drag Handle ---
        self.grip = tk.Frame(self.root, bg="#3a3a3a", width=18, cursor="fleur")
        self.grip.pack(side="left", fill="y")
        self.grip.pack_propagate(False)
        
        self.grip_label = tk.Label(
            self.grip,
            text="⋮\n⋮",
            bg="#3a3a3a",
            fg="#777777",
            font=("Segoe UI", 9, "bold"),
            cursor="fleur"
        )
        self.grip_label.pack(expand=True)
        
        # Dragging handlers
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        
        def start_drag(event):
            self._drag_offset_x = event.x_root - self.root.winfo_x()
            self._drag_offset_y = event.y_root - self.root.winfo_y()
            
        def do_drag(event):
            x = event.x_root - self._drag_offset_x
            y = event.y_root - self._drag_offset_y
            self.root.geometry(f"+{x}+{y}")
            
        for widget in (self.grip, self.grip_label):
            widget.bind("<Button-1>", start_drag)
            widget.bind("<B1-Motion>", do_drag)
            widget.bind("<Enter>", lambda e: (self.grip.config(bg="#484848"), self.grip_label.config(bg="#484848", fg="#cccccc")))
            widget.bind("<Leave>", lambda e: (self.grip.config(bg="#3a3a3a"), self.grip_label.config(bg="#3a3a3a", fg="#777777")))
            
        # --- Content Container ---
        self.content_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        self.idle_text = "what is your command?"
        self.label = tk.Label(self.content_frame, text=self.idle_text, bg="#2d2d2d", fg="white", font=("Segoe UI", 11), padx=10, pady=5)
        self.label.pack(pady=(5, 0))
        
        # Checkbox controls container
        self.controls_frame = tk.Frame(self.content_frame, bg="#2d2d2d")
        self.controls_frame.pack(pady=(0, 5))
        
        # LLM norm checkbox
        self.llm_enabled = False
        def toggle_llm():
            self.llm_enabled = self.use_llm_var.get()
            
        self.use_llm_var = tk.BooleanVar(value=False)
        self.chk_llm = tk.Checkbutton(
            self.controls_frame,
            text="LLM norm",
            variable=self.use_llm_var,
            command=toggle_llm,
            bg="#2d2d2d",
            fg="#aaaaaa",
            selectcolor="#2d2d2d",
            activebackground="#2d2d2d",
            activeforeground="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        self.chk_llm.pack(side="left", padx=4)
        
        # Alert sound checkbox
        self.alert_enabled = True
        def toggle_alert():
            self.alert_enabled = self.use_alert_var.get()
            
        self.use_alert_var = tk.BooleanVar(value=True)
        self.chk_alert = tk.Checkbutton(
            self.controls_frame,
            text="alert",
            variable=self.use_alert_var,
            command=toggle_alert,
            bg="#2d2d2d",
            fg="#aaaaaa",
            selectcolor="#2d2d2d",
            activebackground="#2d2d2d",
            activeforeground="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        self.chk_alert.pack(side="left", padx=4)
        
        # Close button in top-right
        def on_close(event=None):
            self.root.quit()
            
        self.close_btn = tk.Label(self.root, text="×", bg="#2d2d2d", fg="#888888", font=("Segoe UI", 10, "bold"), cursor="hand2")
        self.close_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-3, y=1)
        self.close_btn.bind("<Button-1>", on_close)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(fg="#ff4444"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(fg="#888888"))
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 245
        height = 65
        
        if position == "bottom-right":
            x = screen_width - width - 20
            y = screen_height - height - 60
        elif position == "bottom-left":
            x = 20
            y = screen_height - height - 60
        elif position == "top-center":
            x = (screen_width - width) // 2
            y = 20
        else:
            x = (screen_width - width) // 2
            y = screen_height - height - 60
            
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configure permanent taskbar icon style before showing
        self.setup_taskbar_style()
        
        self.reset_id = None
        self.check_queue()

    def setup_taskbar_style(self):
        """Applies WS_EX_APPWINDOW to ensure permanent taskbar presence."""
        try:
            self.root.update_idletasks()
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if hwnd == 0:
                hwnd = self.root.winfo_id()
                
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception as e:
            print(f"Taskbar style notice: {e}")

    def show_window(self):
        """Displays the ready widget in its exact geometry smoothly."""
        self.root.deiconify()
        self.setup_taskbar_style()

    def reset_to_idle(self):
        self.label.config(text=self.idle_text)
        self.reset_id = None

    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                cmd = msg.get("cmd")
                
                if cmd == "show":
                    if self.reset_id:
                        self.root.after_cancel(self.reset_id)
                        self.reset_id = None
                    self.label.config(text=msg.get("text", ""))
                    
                elif cmd == "show_ready":
                    if self.reset_id:
                        self.root.after_cancel(self.reset_id)
                    self.label.config(text="ready")
                    
                    # Play sound on ready
                    if self.alert_enabled:
                        play_ready_sound()
                        
                    # Return to idle after 5 seconds
                    self.reset_id = self.root.after(5000, self.reset_to_idle)
                    
                elif cmd == "quit":
                    self.root.quit()
                    return
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def run(self):
        self.show_window()
        self.root.mainloop()
