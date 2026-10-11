# -*- coding: utf-8 -*-
# Build: python build.py -> dist/MatrixLock.exe
import subprocess, sys
cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py"]
print("Running:", " ".join(cmd))
sys.exit(subprocess.call(cmd))
