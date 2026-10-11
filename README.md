# Matrix Lock — قفل هوشمند صفحه با افکت ماتریکس

قفل صفحه مدرن، سبک و کاربردی برای زمانی که پای سیستم نیستید — با افکت باران کد ماتریکس، قفل خودکار و پوشش هوشمند صفحه.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5-ff3333?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

### ویژگی‌ها

- **افکت ماتریکس** — باران کاراکترهای روان با رنگ و سرعت قابل تنظیم، تمام‌صفحه و بدون حاشیه
- **قفل خودکار** — اگر به مدت `idle_timeout` ثانیه موس و کیبورد بدون حرکت بماند، خودکار قفل می‌شود
- **پوشش هوشمند صفحه** — بعد از `hide_timeout` ثانیه، جعبه رمز محو می‌شود و فقط ماتریکس + لایه تیره می‌ماند؛ با هر کلید یا حرکت موس دوباره ظاهر می‌شود
- **حفاظت در برابر دور زدن** — مسدودسازی `Win`, `Alt+Tab`, `Alt+F4`, `Ctrl+Esc` و نگه‌داشتن پنجره همیشه روی همه‌چیز (TopMost) همراه با بازگردانی خودکار فوکوس
- **امنیت رمز** — رمز به‌صورت هش SHA256 ذخیره می‌شود و مقایسه با `hmac.compare_digest` انجام می‌شود؛ بعد از ۳ تلاش ناموفق، ۳۰ ثانیه قفل موقت فعال می‌شود
- **انیمیشن نرم** — ظاهر و محو شدن جعبه با Fade، بدون پرش
- **میانبرها** — `Ctrl+Shift+L` قفل دستی، `Enter` تایید رمز، `F2` تغییر رمز (در حالت باز)، `Esc` پاک‌کردن / خروج

> نکته: `Ctrl+Alt+Del` توسط ویندوز (Secure Attention Sequence) قابل مسدودسازی نیست. این محدودیت خود ویندوز است.

---

## نصب و اجرای سریع

```bash
git clone https://github.com/masternewo/matrix-lock.git
cd matrix-lock
pip install -r requirements.txt
python main.py
# رمز پیش‌فرض: 1234
```

### تغییر رمز — ۳ روش

```bash
# ۱) تعاملی
python set_password.py

# ۲) با آرگومان
python set_password.py MyNewPass123

# ۳) داخل برنامه (وقتی قفل باز است) کلید F2
```

### ساخت نسخه EXE (بدون نیاز به پایتون روی مقصد)

```bash
python build.py
# خروجی: dist/MatrixLock.exe
```

فایل آماده را هم می‌توانید از بخش [Releases](../../releases) دانلود کنید. هر Push روی `main` به‌صورت خودکار یک Artifact در تب Actions می‌سازد.

---

## تنظیمات — `config.json`

فایل `config.json` در اولین اجرا خودکار ساخته می‌شود. نمونه در `config.example.json` هست:

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

| کلید | بازه مجاز | توضیح |
|------|-----------|-------|
| `idle_timeout` | 0–3600 | ثانیه بیکاری تا قفل خودکار (۰ = غیرفعال) |
| `hide_timeout` | 0–600 | ثانیه بعد از قفل تا محو شدن جعبه (۰ = غیرفعال) |
| `font_size` | 10–32 | اندازه فونت باران ماتریکس |
| `matrix_speed` | 0.2–3.0 | سرعت حرکت باران |
| `matrix_color` | 0–255 هر کانال | رنگ اصلی باران به صورت RGB |

مقادیر خارج از بازه به‌صورت خودکار اصلاح می‌شوند و برنامه کرش نمی‌کند. لاگ رویدادها در `audit.log` کنار `main.py` ذخیره می‌شود (به گیت نمی‌رود).

---

## ساختار پروژه

```
matrix-lock/
├── main.py                 # برنامه اصلی
├── set_password.py         # ابزار تغییر رمز
├── build.py                # اسکریپت ساخت EXE
├── config.example.json     # نمونه تنظیمات
├── requirements.txt
├── LICENSE
└── .github/workflows/build.yml  # ساخت خودکار EXE
```

## عیب‌یابی

- **صفحه سیاه یا به‌هم‌ریخته؟** `font_size` را کمتر کنید.
- **آنتی‌ویروس هشدار می‌دهد؟** به‌خاطر هوک کیبورد است؛ پوشه را به استثناها اضافه کنید.
- **بیلد Actions قرمز شد؟** تب Actions → آخرین Run → لاگ `Build EXE` را ببینید؛ معمولاً با `pip install` حل می‌شود.

---

ساخته شده با ♥ — [github.com/masternewo/matrix-lock](https://github.com/masternewo/matrix-lock)
