# 🔒 Matrix Lock v2.1 — قفل صفحه ماتریکسی

> قفل صفحه گرافیکی، خفن و امن برای ویندوز — با افکت باران کد ماتریکس + انیمیشن Fade 🌧️💚

![Matrix](https://img.shields.io/badge/Matrix-Rain-00ff41?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5-ff3333?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows)
![Version](https://img.shields.io/badge/Version-2.1-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

### ✨ ویژگی‌ها
- 🎬 **افکت ماتریکس واقعی** — باران کاراکترهای ژاپنی + عدد/حروف با سرعت و رنگ قابل تنظیم
- 🌫️ **انیمیشن Fade نرم** — جعبه قفل نرم محو و ظاهر می‌شود (نه یهویی!)
- 🔐 **قفل امن** — رمز هش SHA256، محو خودکار صفحه بعد از `hide_timeout`
- ⏱️ **قفل خودکار** — بعد `idle_timeout` ثانیه بیکاری خودکار قفل می‌شود
- 👻 **محو صفحه** — بعد `hide_timeout` جعبه محو و فقط ماتریکس می‌ماند (هر کلید/موس بیدارش می‌کند)
- 🛡️ **ضد دور زدن قوی** — `Win`, `Alt+Tab`, `Alt+F4`, `Ctrl+Esc`, `Ctrl+Shift+Esc`, `Menu` مسدود + TOPMOST + فوکوس خودکار
- ⌨️ **میانبرها**
  - `Ctrl+Shift+L` → قفل دستی
  - `Enter` → تایید رمز
  - `F2` → تغییر رمز داخل برنامه (وقتی باز است) 🆕
  - `ESC` → پاک کردن (قفل) / خروج (باز)
- 🎨 **قابل تنظیم** — همه در `config.json`

> ⚠️ **Ctrl+Alt+Del:** به‌دلیل امنیت هسته ویندوز (Secure Attention Sequence) هیچ برنامه عادی نمی‌تواند 100% مسدودش کند. بقیه راه‌ها بسته است.

---

## 🚀 نصب و اجرا

```bash
git clone https://github.com/masternewo/matrix-lock.git
cd matrix-lock
pip install -r requirements.txt
python main.py
# رمز پیش‌فرض: 1234
```

### تغییر رمز (3 روش)
```bash
# 1- تعاملی
python set_password.py
# 2- با آرگومان
python set_password.py MyNewPass123
# 3- داخل برنامه: وقتی باز است F2 بزن
```

### ساخت EXE
```bash
python build.py
# خروجی: dist/MatrixLock.exe
```
یا از [Releases](../../releases) دانلود کن، یا در Actions دستی Run کن تا Release ساخته شود.

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
| کلید | توضیح |
|------|-------|
| `idle_timeout` | بیکاری تا قفل خودکار (0=غیرفعال) |
| `hide_timeout` | بعد قفل تا محو جعبه (0=غیرفعال) |
| `font_size` | سایز باران |
| `matrix_speed` | سرعت (0.5 کند، 2.0 تند) |
| `matrix_color` | رنگ RGB |

---

## 🛠️ ساختار
```
matrix-lock/
├── main.py              # برنامه اصلی v2.1 (Fade + F2)
├── set_password.py      # تغییر رمز (آرگومان + fallback)
├── build.py             # ساخت EXE
├── requirements.txt
├── config.example.json
└── .github/workflows/build.yml
```

## 📦 دانلود
[Releases](../../releases) → `MatrixLock.exe` (~15MB، بدون نیاز به پایتون)

## 🔧 عیب‌یابی
- **صفحه سیاه؟** `font_size` را کم کن
- **آنتی‌ویروس؟** هوک کیبورد دارد، به استثنا اضافه کن
- **Ctrl+Alt+Del؟** محدودیت ویندوز است (توضیح بالا)

---
ساخته شده با ❤️ — `github.com/masternewo/matrix-lock` — v2.1 Fade Edition ✨
