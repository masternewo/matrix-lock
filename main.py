# -*- coding: utf-8 -*-
"""
Matrix Lock - قفل صفحه ماتریکسی ویندوز
خفن، گرافیکی، امن، ضد دور زدن
Ctrl+Alt+Del قابل مسدود سازی کامل نیست (محدودیت ویندوز) ولی بقیه کلیدها مسدود میشن
ساخته شده با Pygame
"""
import pygame
import random
import sys
import os
import json
import hashlib
import time
import ctypes
import threading
from ctypes import wintypes
from datetime import datetime

# ===================== تنظیمات =====================
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_CONFIG = {
    "password_hash": "",  # sha256
    "idle_timeout": 60,  # ثانیه تا قفل خودکار (0 = غیرفعال)
    "hide_timeout": 30,  # ثانیه بعد از قفل تا محو شدن کامل صفحه
    "font_size": 18,
    "matrix_speed": 1.0,
    "matrix_color": [0, 255, 70],
    "hint": "رمز پیشفرض: 1234"
}

WIDTH, HEIGHT = 0, 0

# ===================== ابزارها =====================
def load_config():
    if not os.path.exists(CONFIG_PATH):
        cfg = DEFAULT_CONFIG.copy()
        # رمز پیشفرض 1234
        cfg["password_hash"] = hashlib.sha256("1234".encode()).hexdigest()
        save_config(cfg)
        return cfg
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            if k not in cfg:
                cfg[k] = v
        return cfg
    except:
        return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def get_idle_duration():
    """مدت بیکاری کاربر به ثانیه - ویندوز"""
    try:
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(lii)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    except:
        return 0

def make_topmost():
    try:
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002) # HWND_TOPMOST
        ctypes.windll.user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
    except:
        pass

# ===================== هوک کیبورد (مسدودسازی کلیدهای سیستمی) =====================
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
VK_TAB = 0x09
VK_ESCAPE = 0x1B
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_F4 = 0x73
VK_DELETE = 0x2E

HOOK_HANDLE = None
IS_LOCKED_REF = [False]  # برای اشتراک بین تردها

def low_level_keyboard_proc(nCode, wParam, lParam):
    if nCode == 0 and IS_LOCKED_REF[0]:
        kbd = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_long))
        # lParam -> KBDLLHOOKSTRUCT : vkCode is first DWORD
        vkCode = ctypes.cast(lParam, ctypes.POINTER(wintypes.DWORD))[0]
        # وضعیت کلیدهای خاص
        alt_down = ctypes.windll.user32.GetAsyncKeyState(0x12) & 0x8000
        ctrl_down = ctypes.windll.user32.GetAsyncKeyState(0x11) & 0x8000
        # لیست کلیدهای ممنوعه در حالت قفل
        block = False
        if vkCode in (VK_LWIN, VK_RWIN):
            block = True
        if alt_down and vkCode == VK_TAB: # Alt+Tab
            block = True
        if alt_down and vkCode == VK_F4: # Alt+F4
            block = True
        if ctrl_down and vkCode == VK_ESCAPE: # Ctrl+Esc
            block = True
        if vkCode == VK_ESCAPE: # Esc تنها
            block = True
        # Ctrl+Shift+Esc (Task Manager)
        if ctrl_down and ctypes.windll.user32.GetAsyncKeyState(0x10) & 0x8000 and vkCode == VK_DELETE:
            block = True
        if block:
            return 1
    return ctypes.windll.user32.CallNextHookEx(HOOK_HANDLE, nCode, wParam, lParam)

CMP_FUNC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
HOOK_PROC_PTR = CMP_FUNC(low_level_keyboard_proc)

def install_hook():
    global HOOK_HANDLE
    try:
        HOOK_HANDLE = ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL, HOOK_PROC_PTR, ctypes.windll.kernel32.GetModuleHandleW(None), 0)
        # پیام لوپ برای زنده نگه داشتن هوک
        msg = wintypes.MSG()
        while True:
            ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
    except:
        pass

# ===================== افکت ماتریکس =====================
CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$+-*/=%\"#&_(),.;:?!\|"

class Drop:
    def __init__(self, x, font, speed_mult):
        self.x = x
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(4, 12) * speed_mult
        self.length = random.randint(8, 28)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.font = font
        self.char_size = font.get_height()
        self.switch_timer = random.uniform(0.05, 0.3)
        self.last_switch = time.time()

    def update(self):
        self.y += self.speed
        if self.y - self.length * self.char_size > HEIGHT:
            self.y = random.randint(-200, -20)
            self.length = random.randint(8, 28)
        if time.time() - self.last_switch > self.switch_timer:
            idx = random.randint(0, self.length-1)
            self.chars[idx] = random.choice(CHARS)
            self.last_switch = time.time()

    def draw(self, surf, base_color):
        for i, ch in enumerate(self.chars):
            y = int(self.y - i * self.char_size)
            if 0 <= y < HEIGHT:
                alpha = int(255 * (1 - i / self.length))
                if i == 0:
                    color = (180, 255, 180)  # سر قطره سفید-سبز
                else:
                    r = int(base_color[0] * (1 - i/self.length*0.6))
                    g = int(base_color[1] * (1 - i/self.length*0.2))
                    b = int(base_color[2] * (1 - i/self.length*0.6))
                    color = (r,g,b)
                # سایه برای جذابیت
                try:
                    txt = self.font.render(ch, True, color)
                    txt.set_alpha(alpha)
                    surf.blit(txt, (self.x, y))
                except:
                    pass

# ===================== برنامه اصلی =====================
def main():
    global WIDTH, HEIGHT
    config = load_config()
    pygame.init()
    pygame.font.init()

    # تمام صفحه بدون حاشیه
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    # برای اطمینان رزولوشن درست
    if WIDTH < 800:
        WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.DOUBLEBUF)
    pygame.display.set_caption("Matrix Lock")
    clock = pygame.time.Clock()

    # آیکون و موس
    pygame.mouse.set_visible(False)

    # فونت ها
    try:
        font_matrix = pygame.font.Font(pygame.font.match_font("consolas", bold=False) or pygame.font.get_default_font(), config["font_size"])
    except:
        font_matrix = pygame.font.SysFont("consolas", config["font_size"], bold=False)
    font_big = pygame.font.SysFont("tahoma", 42, bold=True)
    font_mid = pygame.font.SysFont("tahoma", 22)
    font_small = pygame.font.SysFont("tahoma", 16)

    make_topmost()

    # هوک کیبورد در ترد جدا
    t = threading.Thread(target=install_hook, daemon=True)
    t.start()

    # ستون های ماتریکس
    cols = WIDTH // (config["font_size"] + 2)
    drops = [Drop(i*(config["font_size"]+2), font_matrix, config["matrix_speed"]) for i in range(cols)]

    locked = True  # اول قفل باشه - کاربر میتونه با تنظیم idle_timeout عوض کنه
    # اگر رمز خالی بود، پیشفرض 1234
    if not config["password_hash"]:
        config["password_hash"] = hash_password("1234")
        save_config(config)

    input_pw = ""
    message = ""
    msg_color = (255, 255, 100)
    msg_time = 0
    lock_start_time = time.time()
    last_activity = time.time()
    show_box = True

    # برای جلوگیری از Alt+F4 و بستن با X
    running = True

    def draw_lock_ui(surf, hide=False):
        # جعبه وسط
        if hide:
            return
        box_w, box_h = 520, 340
        box_x = (WIDTH - box_w)//2
        box_y = (HEIGHT - box_h)//2
        # پس زمینه شیشه ای
        overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 185))
        pygame.draw.rect(overlay, (0, 255, 70), (0,0,box_w,box_h), 2, border_radius=18)
        surf.blit(overlay, (box_x, box_y))
        # عنوان
        title = font_big.render("🔒  سیستم قفل است", True, (0,255,120))
        surf.blit(title, (box_x + (box_w - title.get_width())//2, box_y + 22))
        sub = font_mid.render("برای ورود رمز را وارد کنید و Enter بزنید", True, (180,255,180))
        surf.blit(sub, (box_x + (box_w - sub.get_width())//2, box_y + 80))
        # ساعت
        now = datetime.now().strftime("%H:%M:%S  -  %Y/%m/%d")
        time_txt = font_mid.render(now, True, (0,255,70))
        surf.blit(time_txt, (box_x + (box_w - time_txt.get_width())//2, box_y + 112))
        # فیلد رمز - ستاره ای
        field_y = box_y + 155
        field_rect = pygame.Rect(box_x+40, field_y, box_w-80, 48)
        pygame.draw.rect(surf, (0,0,0), field_rect, border_radius=10)
        pygame.draw.rect(surf, (0,255,70), field_rect, 2, border_radius=10)
        dots = "●" * len(input_pw)
        if dots == "":
            hint = font_small.render("رمز عبور...", True, (100,180,100))
            surf.blit(hint, (field_rect.x+14, field_rect.y+14))
        else:
            txt = font_mid.render(dots, True, (255,255,255))
            surf.blit(txt, (field_rect.x+14, field_rect.y+10))
            # کرسر چشمک زن
            if int(time.time()*2) % 2 == 0:
                cx = field_rect.x+14+txt.get_width()+4
                pygame.draw.line(surf, (0,255,70), (cx, field_rect.y+10), (cx, field_rect.y+34), 2)
        # پیام
        if message and time.time()-msg_time < 3:
            mtxt = font_small.render(message, True, msg_color)
            surf.blit(mtxt, (box_x + (box_w - mtxt.get_width())//2, field_y+60))
        # راهنما
        help1 = font_small.render("Esc برای پاک کردن  •  Alt+F4 و Win مسدود شد", True, (120,200,120))
        surf.blit(help1, (box_x + (box_w - help1.get_width())//2, box_y + box_h - 52))
        help2 = font_small.render("میانبر قفل دستی: Ctrl+Shift+L  |  خروج امن: رمز درست", True, (90,170,90))
        surf.blit(help2, (box_x + (box_w - help2.get_width())//2, box_y + box_h - 28))
        # هشدار Ctrl+Alt+Del
        warn = font_small.render("نکته: Ctrl+Alt+Del توسط ویندوز مسدود نمیشود (محدودیت امنیتی)", True, (200,200,100))
        surf.blit(warn, ((WIDTH - warn.get_width())//2, HEIGHT - 40))

    while running:
        dt = clock.tick(45)
        IS_LOCKED_REF[0] = locked

        # چک بیکاری برای قفل خودکار وقتی بازه
        if not locked and config["idle_timeout"] > 0:
            if get_idle_duration() >= config["idle_timeout"]:
                locked = True
                lock_start_time = time.time()
                input_pw = ""
                message = "قفل خودکار فعال شد"
                msg_color = (0,255,120)
                msg_time = time.time()
                pygame.mouse.set_visible(False)
                make_topmost()

        # اگر قفل بود و مدت زیادی گذشت، صفحه را کامل بپوشان (hide box)
        if locked:
            elapsed = time.time() - lock_start_time
            if elapsed > config["hide_timeout"] and config["hide_timeout"] > 0:
                # بعد hide_timeout جعبه ورودی محو میشه و فقط ماتریکس + سیاهی میمونه
                # برای نمایش دوباره، کاربر کافیه یک کلید بزنه
                if input_pw == "" and not any(pygame.key.get_pressed()):
                    show_box = False
                else:
                    show_box = True
                    lock_start_time = time.time() # ریست اگر تعامل کرد
            else:
                show_box = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if locked:
                    # اجازه بستن نده
                    message = "در حالت قفل نمیتوان بست! رمز را وارد کنید"
                    msg_color = (255,80,80)
                    msg_time = time.time()
                    make_topmost()
                else:
                    running = False
            elif event.type == pygame.KEYDOWN:
                # میانبر قفل دستی Ctrl+Shift+L
                mods = pygame.key.get_mods()
                if event.key == pygame.K_l and (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT):
                    if not locked:
                        locked = True
                        lock_start_time = time.time()
                        input_pw = ""
                        pygame.mouse.set_visible(False)
                        message = "قفل دستی فعال شد"
                        msg_color = (0,255,120)
                        msg_time = time.time()
                    continue
                if not locked:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    continue
                # در حالت قفل: ورودی رمز
                show_box = True
                lock_start_time = time.time()
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if hash_password(input_pw) == config["password_hash"]:
                        locked = False
                        input_pw = ""
                        message = ""
                        pygame.mouse.set_visible(True)
                        # یک لحظه افکت باز شدن
                    else:
                        message = "❌ رمز نادرست! دوباره تلاش کنید"
                        msg_color = (255,70,70)
                        msg_time = time.time()
                        input_pw = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_pw = input_pw[:-1]
                elif event.key == pygame.K_ESCAPE:
                    input_pw = ""
                    message = "پاک شد"
                    msg_color = (200,200,100)
                    msg_time = time.time()
                else:
                    # فقط کاراکترهای قابل چاپ
                    if event.unicode and len(input_pw) < 32 and ord(event.unicode) >= 32:
                        input_pw += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if locked:
                    show_box = True
                    lock_start_time = time.time()
                    make_topmost()

        # نگه داشتن پنجره همیشه بالا و فوکوس
        if locked:
            try:
                hwnd = pygame.display.get_wm_info()["window"]
                # اگر فوکوس از دست رفت، برگردان
                if ctypes.windll.user32.GetForegroundWindow() != hwnd:
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0,0,0,0, 0x0001|0x0002|0x0010)
                # جلوگیری از Win+D و ... با تاخیر کم
            except:
                pass

        # رندر
        screen.fill((0,0,0))
        # ماتریکس همیشه در پس زمینه
        for d in drops:
            d.update()
            d.draw(screen, tuple(config["matrix_color"]))
        # لایه تاریکی برای خوانایی
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,60))
        screen.blit(dim, (0,0))

        if locked:
            # اگر hide شد، فقط ماتریکس + نوار سیاه کامل بعد از تایم؟
            if not show_box:
                # پوشش کامل سیاه شفاف + متن کوچک "برای بیدار شدن کلیدی بزنید"
                cover = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                cover.fill((0,0,0,180))
                screen.blit(cover, (0,0))
                wake = font_mid.render("برای بیداری صفحه یک کلید بزنید...", True, (0,255,70))
                screen.blit(wake, ((WIDTH-wake.get_width())//2, HEIGHT//2))
                # ماتریکس کم رنگ پشت
            else:
                draw_lock_ui(screen, hide=False)
        else:
            # حالت باز - داشبورد ساده
            panel = pygame.Surface((560, 220), pygame.SRCALPHA)
            panel.fill((0,20,0,160))
            pygame.draw.rect(panel, (0,255,70), (0,0,560,220), 2, border_radius=16)
            screen.blit(panel, ((WIDTH-560)//2, (HEIGHT-220)//2))
            t1 = font_big.render("✅  سیستم باز است", True, (0,255,120))
            screen.blit(t1, ((WIDTH - t1.get_width())//2, HEIGHT//2 - 60))
            t2 = font_mid.render("برای قفل: Ctrl+Shift+L  یا منتظر قفل خودکار بمانید", True, (180,255,180))
            screen.blit(t2, ((WIDTH - t2.get_width())//2, HEIGHT//2 + 5))
            t3 = font_small.render(f"قفل خودکار: {config['idle_timeout']} ثانیه بیکاری  |  رمز را در config.json عوض کنید", True, (120,200,120))
            screen.blit(t3, ((WIDTH - t3.get_width())//2, HEIGHT//2 + 45))
            t4 = font_small.render("ESC برای خروج  •  برای تست قفل، کلید میانبر را بزنید", True, (90,170,90))
            screen.blit(t4, ((WIDTH - t4.get_width())//2, HEIGHT//2 + 75))

        # واترمارک
        wm = font_small.render("Matrix Lock v1.0  |  github.com/masternewo/matrix-lock", True, (0,180,70))
        screen.blit(wm, (14, HEIGHT-24))
        pygame.display.flip()

    pygame.quit()
    try:
        if HOOK_HANDLE:
            ctypes.windll.user32.UnhookWindowsHookEx(HOOK_HANDLE)
    except:
        pass
    sys.exit(0)

if __name__ == "__main__":
    main()
