import pyperclip

class Typer:
    def type_text(self, text, prepend_clipboard=False):
        if not text:
            return
            
        if prepend_clipboard:
            try:
                old_clip = pyperclip.paste()
                if old_clip and old_clip.strip():
                    text = f"{text}\n\n{old_clip}"
            except Exception as e:
                print(f"[Typer] Clipboard read error: {e}")

        # Просто помещаем готовый текст в буфер обмена
        pyperclip.copy(text)
