# Security Policy - Matrix Lock MIL-SPEC v2.3

## 🛡️ سطح امنیتی
این پروژه با فرض **MIL-SPEC** طراحی شده است.

### اقدامات امنیتی پیاده‌سازی شده
- ✅ **Timing-safe password compare**: `hmac.compare_digest()` ضد timing-attack
- ✅ **Brute-Force Protection**: ۳ تلاش ناموفق → ۳۰ ثانیه قفل کامل + شمارش معکوس
- ✅ **Audit Trail**: تمام رویدادها در `audit.log` با timestamp
  - `SYSTEM_START`, `LOGIN_SUCCESS`, `LOGIN_FAIL`, `LOCKOUT_ACTIVATED`, `AUTO_LOCK`, `MANUAL_LOCK`, `PASSWORD_CHANGED`, `BLOCK_CLOSE_ATTEMPT`
- ✅ **Input Validation**: `validate_config()` با clamp رنج برای تمام پارامترها (جلوگیری از کرش با config خراب)
- ✅ **TOPMOST Hardened**: `HWND_TOPMOST` + `SWP_SHOWWINDOW` + `SetForegroundWindow` هر ثانیه
- ✅ **Keyboard Hook**: مسدودسازی `Win`, `Alt+Tab`, `Alt+F4`, `Ctrl+Esc`, `Ctrl+Shift+Esc`, `Menu`
- ✅ **Secrets Protection**: `.gitignore` نظامی - `config.json` و `audit.log` هرگز کامیت نمی‌شوند
- ✅ **Fallback Safe**: تمام بخش‌های حساس در `try/except` - برنامه کرش نمی‌کند

### ⚠️ محدودیت شناخته شده (By Design)
`Ctrl+Alt+Del` (Secure Attention Sequence) توسط هسته ویندوز برای هیچ برنامه user-mode قابل مسدودسازی نیست. این محدودیت امنیتی ویندوز است، نه ضعف برنامه. برای امنیت فیزیکی کامل از `Win+L` یا Screensaver mode استفاده کنید.

## 📜 Audit Log
فایل `audit.log` در کنار `main.py` ساخته می‌شود:
```
[2026-10-11 02:48:00] SYSTEM_START locked=true
[2026-10-11 02:48:12] LOGIN_FAIL attempt 1/3 success=False
[2026-10-11 02:48:20] LOCKOUT_ACTIVATED 30s
[2026-10-11 02:48:55] LOGIN_SUCCESS success=True
```
این فایل به گیت نمی‌رود (.gitignore) و حاوی رمز نیست.

## 🔐 گزارش آسیب‌پذیری
اگر آسیب‌پذیری پیدا کردید، لطفاً Issue باز کنید یا به masternewo گزارش دهید. وصله در شاخه `main` منتشر می‌شود.

## 📦 نسخه
- v2.3 MIL-SPEC (current)
- v2.1 Fade Edition
- v2.0 Initial
