# -*- coding: utf-8 -*-
"""ساخت MatrixLock.exe با PyInstaller v2.3 MIL-SPEC"""
import subprocess, sys, os

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--noconsole",
    "--clean",
    "--name", "MatrixLock",
    "main.py"
]
if os.path.exists("icon.ico"):
    cmd.extend(["--icon", "icon.ico"])

print("🔨 Build:", " ".join(cmd))
ret = subprocess.call(cmd)
if ret == 0:
    # چک خروجی
    import glob
    files = glob.glob("dist/*")
    print(f"✅ Done! dist: {files}")
    exe = "dist/MatrixLock.exe"
    if os.path.exists(exe):
        print(f"📦 {exe} {os.path.getsize(exe)/1024/1024:.1f} MB")
else:
    print("❌ Build failed")
    sys.exit(ret)
