import os
import sys
import re

DEFAULT_GLOSSARY_TEMPLATE = """# Shockwave Glossary / Пользовательский словарь замен
# Формат: шаблон = замена
# Замена производится без учета регистра (case-insensitive) с границами слов.
# Файл можно редактировать на лету — изменения подхватываются автоматически.
# Строки с решеткой (#) или пустые строки игнорируются.

# Примеры для IT, разработки и трейдинга:
докер = Docker
кубер = Kubernetes
кубернетес = Kubernetes
тайпскрипт = TypeScript
джаваскрипт = JavaScript
питон = Python
гитхаб = GitHub
тайгер трейд = Tiger.Trade
бинанс = Binance
промпт = промпт
"""

class GlossaryManager:
    def __init__(self, glossary_path=None):
        if glossary_path is None:
            if getattr(sys, 'frozen', False):
                exe_dir = os.path.dirname(sys.executable)
                self.glossary_path = os.path.join(exe_dir, "glossary.txt")
            else:
                self.glossary_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "glossary.txt")
                )
        else:
            self.glossary_path = glossary_path

        self._last_mtime = 0
        self._rules = []
        self._ensure_file_exists()
        self.reload()

    def _ensure_file_exists(self):
        """Creates a default glossary.txt template if the file doesn't exist yet."""
        if not os.path.exists(self.glossary_path):
            try:
                with open(self.glossary_path, "w", encoding="utf-8") as f:
                    f.write(DEFAULT_GLOSSARY_TEMPLATE)
            except Exception as e:
                print(f"[Glossary] Error creating default glossary file: {e}")

    def reload(self):
        """Parses glossary.txt and compiles regex patterns if the file was modified."""
        if not os.path.exists(self.glossary_path):
            self._rules = []
            return

        try:
            mtime = os.path.getmtime(self.glossary_path)
            if mtime == self._last_mtime and self._rules:
                return

            self._last_mtime = mtime
            rules = []

            with open(self.glossary_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        pattern, replacement = line.split("=", 1)
                        pattern = pattern.strip()
                        replacement = replacement.strip()
                        if pattern and replacement:
                            rules.append((pattern, replacement))

            # Sort rules by pattern length descending to replace longer phrases first
            rules.sort(key=lambda r: len(r[0]), reverse=True)

            compiled_rules = []
            for pattern, replacement in rules:
                # Use unicode-safe word boundaries (?<!\w) and (?!\w)
                regex = re.compile(
                    r'(?<!\w)' + re.escape(pattern) + r'(?!\w)',
                    re.IGNORECASE | re.UNICODE
                )
                compiled_rules.append((regex, replacement))

            self._rules = compiled_rules
        except Exception as e:
            print(f"[Glossary] Error reading glossary file: {e}")

    def apply(self, text: str) -> str:
        """Applies glossary substitution rules to text."""
        if not text:
            return text

        self.reload()
        if not self._rules:
            return text

        result = text
        for regex, replacement in self._rules:
            result = regex.sub(replacement, result)

        return result
