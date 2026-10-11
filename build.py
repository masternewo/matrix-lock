# -*- coding: utf-8 -*-
"""ساخت فایل اجرایی Matrix Lock"""
import subprocess
import sys

def main():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "MatrixLock",
        "main.py",
    ]
    print("Build command:", " ".join(cmd))
    ret = subprocess.call(cmd)
    if ret != 0:
        print("Build failed")
        sys.exit(ret)
    print("Build finished - check dist/MatrixLock.exe")

if __name__ == "__main__":
    main()
