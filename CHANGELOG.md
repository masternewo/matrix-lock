# Changelog - Matrix Lock

## v2.3 MIL-SPEC (2026-10-11) - نظامی
- ✅ `hmac.compare_digest` ضد timing-attack
- ⛔ Brute-Force: 3x → 30s lockout + countdown
- 📜 `audit.log` با timestamp برای تمام رویدادها
- ✅ `validate_config()` با clamp رنج (idle 0-3600, hide 0-600, font 10-32, speed 0.2-3.0)
- 🛡️ TOPMOST hardened (HWND_TOPMOST + SHOWWINDOW + Foreground)
- 📜 LICENSE MIT + Security Notice
- 🛡️ .gitignore نظامی (config.json + audit.log never commit)
- ⚙️ build.yml v2.3 با 3 مرحله validation + verify EXE

## v2.2 MIL-SPEC Step 3-1
- Brute-Force + hmac اولیه

## v2.1 Fade Edition (2026-10-11)
- 🌫️ Fade نرم جعبه قفل (box_alpha)
- ⌨️ F2 تغییر رمز داخل برنامه
- 🖱️ موس هم بیدار می‌کند
- 🛡️ Menu key مسدود + پایداری بیشتر

## v2.0 Initial
- باران ماتریکس، قفل خودکار، محو صفحه، هوک کیبورد، TOPMOST
