# -*- coding: utf-8 -*-
"""ابزار تغییر رمز Matrix Lock v2.1"""
import os, json, hashlib, getpass, sys

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def hash_pw(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def ask_password(prompt):
    try:
        return getpass.getpass(prompt)
    except:
        # fallback اگر getpass در IDE کار نکرد
        return input(prompt)

def main():
    print("🔒 Matrix Lock v2.1 - تغییر رمز")
    print("-"*45)
    # اگر آرگومان داده شد: python set_password.py mypass123
    if len(sys.argv) > 1:
        pw1 = sys.argv[1]
        pw2 = pw1
        print(f"ℹ️ رمز از آرگومان گرفته شد: {'*'*len(pw1)}")
    else:
        pw1 = ask_password("رمز جدید را وارد کنید: ")
        pw2 = ask_password("تکرار رمز جدید: ")
        # اگر خالی بود دوباره با input
        if not pw1:
            pw1 = input("رمز جدید (نمایش داده میشود): ")
            pw2 = input("تکرار: ")

    if pw1 != pw2:
        print("❌ رمزها یکسان نیست!")
        sys.exit(1)
    if len(pw1) < 4:
        print("❌ رمز حداقل 4 کاراکتر باشد")
        sys.exit(1)

    h = hash_pw(pw1)
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            cfg = {}

    cfg["password_hash"] = h
    defaults = {"idle_timeout":60,"hide_timeout":30,"font_size":18,"matrix_speed":1.0,"matrix_color":[0,255,70],"hint":""}
    for k,v in defaults.items():
        if k not in cfg:
            cfg[k]=v

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    print(f"✅ رمز با موفقیت تغییر کرد!")
    print(f"هش: {h}")
    print(f"📁 ذخیره شد: {CONFIG_PATH}")
    print(f"💡 برای تست: python main.py  (رمز: {'*'*len(pw1)})")

if __name__=="__main__":
    main()
