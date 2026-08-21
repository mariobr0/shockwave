import pyperclip

class Typer:
    def type_text(self, text):
        if not text:
            return
            
        # Просто помещаем готовый текст в буфер обмена
        pyperclip.copy(text)
