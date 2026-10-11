# Build MatrixLock.exe
# Usage: python build.py  -> dist/MatrixLock.exe
import subprocess
import sys

cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py"]
print("Build:", " ".join(cmd))
raise SystemExit(subprocess.call(cmd))
