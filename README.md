# 🔒 Matrix Lock v2.3 MIL-SPEC — قفل صفحه ماتریکسی نظامی

> قفل صفحه گرافیکی، خفن و امن در سطح فرض نظامی — باران ماتریکس + Fade + ضد Brute-Force + آدیت‌لاگ 🌧️🛡️

![Matrix](https://img.shields.io/badge/Matrix-Rain-00ff41?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5-ff3333?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows)
![Version](https://img.shields.io/badge/Version-v2.3_MIL--SPEC-red?style=flat-square)
![MIL-SPEC](https://img.shields.io/badge/MIL--SPEC-PASSED-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

### 🛡️ ویژگی‌های نظامی v2.3
- 🎬 **ماتریکس واقعی** — باران کاتاکانا + سرعت/رنگ قابل تنظیم
- 🌫️ **Fade نرم** — جعبه با `box_alpha` محو/ظاهر می‌شود
- 🔐 **hmac امن** — `hmac.compare_digest` ضد timing-attack
- ⛔ **ضد Brute-Force** — ۳ بار اشتباه → ۳۰ ثانیه قفل کامل + شمارش معکوس
- 📜 **آدیت‌لاگ** — همه لاگین‌ها/خطاها در `audit.log` با timestamp
- ✅ **اعتبارسنجی Config** — رنج عددی، clamp رنگ، جلوگیری از کرش با config خراب
- 🛡️ **ضد دور زدن** — `Win`, `Alt+Tab`, `Alt+F4`, `Ctrl+Esc`, `Ctrl+Shift+Esc`, `Menu` مسدود + TOPMOST قوی + بازگردانی فوکوس
- 👻 **محو صفحه** — بعد `hide_timeout` جعبه محو، هر کلید/موس بیدار می‌کند
- ⌨️ **میانبرها**: `Ctrl+Shift+L` قفل دستی، `F2` تغییر رمز داخل برنامه، `Enter` تایید
- 🔒 **.gitignore نظامی** — `config.json` و `audit.log` هرگز کامیت نمی‌شوند

> ⚠️ **Ctrl+Alt+Del:** توسط هسته ویندوز (SAS) برای هیچ برنامه user-mode قابل بلوکه نیست — این محدودیت امنیتی ویندوز است، نه ضعف برنامه.

---

## 🚀 نصب و اجرا

```bash
git clone https://github.com/masternewo/matrix-lock.git
cd matrix-lock
pip install -r requirements.txt
python main.py
# رمز پیش‌فرض: 1234
```

### تغییر رمز
```bash
python set_password.py
python set_password.py MyNewPass123
# یا داخل برنامه وقتی باز است: F2
```

### ساخت EXE
```bash
python build.py
# → dist/MatrixLock.exe (~15MB)
```

---

## ⚙️ config.json

```json
{
  "password_hash": "...sha256...",
  "idle_timeout": 60,
  "hide_timeout": 30,
  "font_size": 18,
  "matrix_speed": 1.0,
  "matrix_color": [0, 255, 70]
}
```
| کلید | رنج نظامی | توضیح |
|------|-----------|-------|
| `idle_timeout` | 0-3600 | بیکاری تا قفل (0=غیرفعال) |
| `hide_timeout` | 0-600 | تاخیر تا محو جعبه |
| `font_size` | 10-32 | سایز باران |
| `matrix_speed` | 0.2-3.0 | سرعت |
| `matrix_color` | 0-255 | RGB |

فایل خراب یا رنج اشتباه خودکار اصلاح (clamp) می‌شود — کرش نمی‌کند.

---

## 📜 آدیت‌لاگ (audit.log)

```
[2026-10-11 02:48:00] SYSTEM_START locked=true
[2026-10-11 02:48:12] LOGIN_FAIL attempt 1/3 success=False
[2026-10-11 02:48:20] LOCKOUT_ACTIVATED 30s
[2026-10-11 02:48:55] LOGIN_SUCCESS success=True
```

## 🛠️ ساختار

```
├── main.py              # v2.3 MIL-SPEC (hmac + brute-force + audit + validate)
├── set_password.py
├── build.py
├── config.example.json
├── LICENSE              # MIT + Security Notice
├── requirements.txt
└── .github/workflows/build.yml
```

## 📦 دانلود

[Releases](../../releases) → `MatrixLock.exe`

## 🔧 عیب‌یابی

- **صفحه سیاه؟** `font_size` را کم کن (ولیدیتور خودکار 10-32 می‌کند)
- **آنتی‌ویروس؟** هوک کیبورد دارد، به استثنا اضافه کن
- **audit.log کجاست؟** کنار `main.py` — هرگز به گیت نمی‌رود (.gitignore)

---
**استاندارد:** MIL-SPEC فرضی — timing-safe, brute-force lockout, audit trail, input validation ✅
ساخته شده با ❤️ — `github.com/masternewo/matrix-lock` — v2.3 MIL-SPEC ✨
