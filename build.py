# -*- coding: utf-8 -*-
"""Build MatrixLock EXE - python build.py"""
import subprocess, sys, os
cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py", "--log-level", "WARN"]
print("Running:", " ".join(cmd))
ret = subprocess.call(cmd)
if ret != 0:
    print("Build failed", ret)
    sys.exit(ret)
exe = os.path.join("dist", "MatrixLock.exe")
if os.path.exists(exe):
    print(f"OK -> {exe} {os.path.getsize(exe)/1024/1024:.1f} MB")
else:
    try:
        print("dist:", os.listdir("dist"))
    except Exception as e:
        print(e)
