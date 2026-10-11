# 🔒 Matrix Lock — قفل صفحه ماتریکسی

> قفل صفحه گرافیکی، خفن و امن برای ویندوز — با افکت باران کد ماتریکس 🌧️💚

![Matrix](https://img.shields.io/badge/Matrix-Rain-00ff41?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5-ff3333?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

### ✨ ویژگی‌ها
- 🎬 **افکت ماتریکس واقعی** — باران کاراکترهای ژاپنی + عدد/حروف با سرعت و رنگ قابل تنظیم
- 🔐 **قفل امن** — رمز عبور هش شده (SHA256)، محو خودکار صفحه بعد از `hide_timeout`
- ⏱️ **قفل خودکار** — وقتی `idle_timeout` ثانیه موس/کیبورد بیکار باشد خودکار قفل می‌شود
- 👻 **محو صفحه** — بعد از `hide_timeout` ثانیه جعبه رمز محو و فقط ماتریکس + پرده سیاه می‌ماند (با هر کلید بیدار می‌شود)
- 🛡️ **ضد دور زدن قوی**
  - مسدود: `Win`, `Alt+Tab`, `Alt+F4`, `Ctrl+Esc`, `Ctrl+Shift+Esc`, `Esc`
  - همیشه روی همه پنجره‌ها (`TOPMOST`) + بازگردانی فوکوس خودکار هر 300ms
  - جلوگیری از بستن با `X` در حالت قفل
- ⌨️ **میانبرها**
  - `Ctrl+Shift+L` → قفل دستی
  - `Enter` → تایید رمز
  - `F2` → تغییر رمز (در حالت باز)
  - `ESC` → پاک کردن ورودی (قفل) / خروج (باز)
- 🎨 **قابل تنظیم** — همه چیز در `config.json` (رمز، تایمرها، سرعت، رنگ)
- 🖥️ **تمام صفحه بدون حاشیه** — `NOFRAME` + `TOPMOST` + `MAXIMIZE`

> ⚠️ **نکته مهم Ctrl+Alt+Del:** ترکیب `Ctrl+Alt+Del` به دلیل امنیت هسته ویندوز (Secure Attention Sequence) توسط هیچ برنامه عادی قابل مسدودسازی 100% نیست. ویندوز فقط به Credential Provider اجازه این کار را می‌دهد. این برنامه بقیه راه‌های دور زدن را می‌بندد و برای Ctrl+Alt+Del هشدار می‌دهد. برای امنیت کامل، از `Win+L` ویندوز یا اجرای برنامه به عنوان Screensaver استفاده کنید.

---

## 🚀 نصب و اجرا

### اجرای سریع (بدون نصب)
```bash
git clone https://github.com/masternewo/matrix-lock.git
cd matrix-lock
pip install -r requirements.txt
python main.py
```
رمز پیش‌فرض: `1234`

### تغییر رمز
```bash
python set_password.py
# یا دستی: فایل config.json -> مقدار password_hash را عوض کنید
```
یا داخل برنامه وقتی باز است کلید `F2` را بزنید.

### ساخت فایل EXE (بدون نیاز به پایتون)
```bash
pip install pyinstaller
python build.py
# خروجی: dist/MatrixLock.exe
```
یا از Release آماده دانلود کنید.

---

## ⚙️ تنظیمات `config.json`
```json
{
  "password_hash": "...sha256...",
  "idle_timeout": 60,
  "hide_timeout": 30,
  "font_size": 18,
  "matrix_speed": 1.0,
  "matrix_color": [0, 255, 70],
  "hint": "رمز پیشفرض: 1234"
}
```
| کلید | توضیح |
|------|-------|
| `idle_timeout` | ثانیه بیکاری تا قفل خودکار (0=غیرفعال) |
| `hide_timeout` | ثانیه بعد از قفل تا محو جعبه (0=غیرفعال) |
| `font_size` | سایز فونت باران |
| `matrix_speed` | سرعت باران (مثلاً 0.5 کند، 2.0 تند) |
| `matrix_color` | رنگ اصلی RGB |

---

## 🛠️ ساختار پروژه
```
matrix-lock/
├── main.py              # برنامه اصلی
├── set_password.py      # ابزار تغییر رمز
├── build.py             # اسکریپت ساخت EXE
├── requirements.txt
├── config.json          # تنظیمات (ساخته می‌شود)
├── config.example.json  # نمونه تنظیمات
└── .github/workflows/build.yml  # ساخت خودکار EXE
```

## 📦 دانلود EXE آماده
به بخش [Releases](../../releases) بروید و `MatrixLock.exe` را دانلود کنید.

## 🔧 عیب‌یابی
- **صفحه سیاه؟** رزولوشن شما گرفته شده، `font_size` را کم کنید.
- **آنتی‌ویروس گیر می‌دهد؟** چون هوک کیبورد دارد؛ پوشه را به استثنا اضافه کنید.
- **Ctrl+Alt+Del باز می‌شود؟** توضیح بالا را بخوانید — محدودیت ویندوز است.

---

ساخته شده با ❤️ و افکت ماتریکس — `github.com/masternewo/matrix-lock`
