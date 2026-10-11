# -*- coding: utf-8 -*-
"""Build MatrixLock EXE - python build.py"""
import subprocess
import sys
import os

def main():
    # اطمینان از نصب بودن بسته‌ها
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "MatrixLock",
        "--log-level", "WARN",
        "main.py",
    ]
    print("Running:", " ".join(cmd))
    ret = subprocess.call(cmd)
    if ret != 0:
        print(f"Build failed with exit code {ret}")
        sys.exit(ret)
    exe = os.path.join("dist", "MatrixLock.exe")
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024*1024)
        print(f"OK -> {exe} ({size_mb:.1f} MB)")
    else:
        print("WARNING: dist/MatrixLock.exe not found - check log above")
        # لیست dist برای عیب‌یابی
        try:
            print("dist contents:", os.listdir("dist"))
        except Exception as e:
            print("dist error:", e)

if __name__ == "__main__":
    main()
