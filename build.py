# -*- coding: utf-8 -*-
import subprocess, sys
subprocess.call([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", "MatrixLock", "main.py"])
