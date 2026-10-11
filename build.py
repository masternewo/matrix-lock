# -*- coding: utf-8 -*-
"""Build script - pyinstaller onefile"""
import subprocess, sys
cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py"]
print(" ".join(cmd))
raise SystemExit(subprocess.call(cmd))
