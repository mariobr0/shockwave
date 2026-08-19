import tkinter as tk
import queue

class WinVoiceUI:
    def __init__(self, message_queue, position="bottom-left"):
        self.queue = message_queue
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#2d2d2d")
        
        self.label = tk.Label(self.root, text="", bg="#2d2d2d", fg="white", font=("Segoe UI", 12), padx=15, pady=5)
        self.label.pack(pady=(5, 0))
        
        self.llm_enabled = False
        
        def toggle_llm():
            self.llm_enabled = self.use_llm_var.get()
            
        self.use_llm_var = tk.BooleanVar(value=False)
        self.chk = tk.Checkbutton(
            self.root,
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
        self.chk.pack(pady=(0, 5))
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 140
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
        # self.root.withdraw()  # Removed so it shows immediately on startup

        
        self.fade_id = None
        self.check_queue()

    def do_fade(self):
        alpha = self.root.attributes("-alpha")
        if alpha > 0:
            self.root.attributes("-alpha", max(0, alpha - 0.05))
            self.fade_id = self.root.after(50, self.do_fade)
        else:
            self.root.withdraw()
            self.root.attributes("-alpha", 0.9)
            self.fade_id = None

    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                cmd = msg.get("cmd")
                if cmd == "show":
                    if self.fade_id:
                        self.root.after_cancel(self.fade_id)
                        self.fade_id = None
                    self.root.attributes("-alpha", 0.9)
                    self.label.config(text=msg.get("text", ""))
                    self.root.deiconify()
                elif cmd == "fade_out":
                    self.label.config(text=msg.get("text", ""))
                    self.root.deiconify()
                    self.root.attributes("-alpha", 0.9)
                    if self.fade_id:
                        self.root.after_cancel(self.fade_id)
                    # Schedule fade after 7 seconds
                    self.fade_id = self.root.after(7000, self.do_fade)
                elif cmd == "hide":
                    self.root.withdraw()
                elif cmd == "quit":
                    self.root.quit()
                    return
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def run(self):
        self.root.mainloop()
