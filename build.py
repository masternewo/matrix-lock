# -*- coding: utf-8 -*-
"""Build MatrixLock EXE - run: python build.py"""
import subprocess
import sys

cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py"]
print("Running:", " ".join(cmd))
ret = subprocess.call(cmd)
if ret != 0:
    print("Build failed with code", ret)
    sys.exit(ret)
print("Done. Output: dist/MatrixLock.exe")
