#!/usr/bin/env python3
import sys
from pathlib import Path

# Enable UTF-8 console output
sys.stdout.reconfigure(encoding="utf-8")

ansi_file = Path(__file__).with_name("shockwave_transparent.ansi")
if ansi_file.exists():
    print(ansi_file.read_text(encoding="utf-8"))
else:
    print(f"File not found: {ansi_file}")
