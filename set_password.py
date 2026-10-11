# -*- coding: utf-8 -*-
"""ابزار تغییر رمز Matrix Lock"""
import os, json, hashlib, getpass

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def main():
    print("🔒 Matrix Lock - تغییر رمز")
    print("-"*40)
    pw1 = getpass.getpass("رمز جدید را وارد کنید: ")
    pw2 = getpass.getpass("تکرار رمز جدید: ")
    if pw1 != pw2:
        print("❌ رمزها یکسان نیست!")
        return
    if len(pw1) < 4:
        print("❌ رمز حداقل 4 کاراکتر باشد")
        return
    h = hash_pw(pw1)
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except: cfg = {}
    cfg["password_hash"] = h
    # مقادیر پیشفرض اگر نبود
    defaults = {"idle_timeout":60,"hide_timeout":30,"font_size":18,"matrix_speed":1.0,"matrix_color":[0,255,70],"hint":""}
    for k,v in defaults.items():
        if k not in cfg: cfg[k]=v
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"✅ رمز با موفقیت تغییر کرد!\nهش: {h}")
    print(f"فایل ذخیره شد: {CONFIG_PATH}")

if __name__=="__main__":
    main()
