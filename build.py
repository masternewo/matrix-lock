# -*- coding: utf-8 -*-
"""ساخت MatrixLock.exe با PyInstaller v2.1"""
import os, subprocess, sys

def build():
    sep = ";" if os.name == "nt" else ":"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "MatrixLock",
        "--add-data", f"config.example.json{sep}.",
        "main.py"
    ]
    # آیکون اگر وجود داشت
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon")
        cmd.insert(-1, "icon.ico")

    print("🔨 در حال ساخت MatrixLock.exe ...")
    print(" ".join(cmd))
    ret = subprocess.call(cmd)
    if ret == 0:
        exe = "dist/MatrixLock.exe" if os.name=="nt" else "dist/MatrixLock"
        if os.path.exists(exe):
            size = os.path.getsize(exe)/1024/1024
            print(f"\n✅ ساخت موفق! → {exe} ({size:.1f} MB)")
            print("💡 اجرا: dist/MatrixLock.exe")
        else:
            # لینوکس خروجی بدون exe
            import glob
            files = glob.glob("dist/*")
            print(f"✅ ساخت تمام! فایل‌ها: {files}")
    else:
        print("❌ خطا در ساخت - لاگ بالا را چک کن")
        sys.exit(ret)

if __name__ == "__main__":
    build()
