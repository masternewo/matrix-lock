# -*- coding: utf-8 -*-
"""ساخت MatrixLock.exe با PyInstaller"""
import os, subprocess, sys, shutil

CMD = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--noconsole",
    "--name", "MatrixLock",
    "--icon", "NONE",
    "--add-data", "config.example.json;.",
    "main.py"
]
# روی لینوکس/مک جداکننده : است
if os.name != "nt":
    CMD[CMD.index("--add-data")+1] = "config.example.json:."

print("🔨 در حال ساخت MatrixLock.exe ...")
print(" ".join(CMD))
ret = subprocess.call(CMD)
if ret==0:
    print("\n✅ ساخت موفق! فایل در dist/MatrixLock.exe")
    if os.path.exists("dist/MatrixLock.exe"):
        size = os.path.getsize("dist/MatrixLock.exe")/1024/1024
        print(f"حجم: {size:.1f} MB")
else:
    print("❌ خطا در ساخت")
    sys.exit(ret)
