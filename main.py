# -*- coding: utf-8 -*-
"""
Matrix Lock v2.1 - قفل صفحه ماتریکسی ویندوز
- افکت باران کد ماتریکس گرافیکی
- انیمیشن محو شدن نرم (Fade) برای جعبه قفل
- قفل خودکار + محو صفحه بعد از hide_timeout
- ضد دور زدن: Win, Alt+Tab, Alt+F4, Ctrl+Esc, Ctrl+Shift+Esc
- همیشه TOPMOST + بازگردانی فوکوس
نکته: Ctrl+Alt+Del توسط ویندوز قابل مسدودسازی نیست (Secure Attention Sequence)
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
    "password_hash": "",
    "idle_timeout": 60,
    "hide_timeout": 30,
    "font_size": 18,
    "matrix_speed": 1.0,
    "matrix_color": [0, 255, 70],
    "hint": "رمز پیشفرض: 1234"
}

WIDTH, HEIGHT = 0, 0

def load_config():
    if not os.path.exists(CONFIG_PATH):
        cfg = DEFAULT_CONFIG.copy()
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
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except:
        pass

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def get_idle_duration():
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
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        ctypes.windll.user32.ShowWindow(hwnd, 3)
    except:
        pass

# ===================== هوک کیبورد =====================
WH_KEYBOARD_LL = 13
VK_TAB = 0x09
VK_ESCAPE = 0x1B
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_F4 = 0x73
VK_DELETE = 0x2E

HOOK_HANDLE = None
IS_LOCKED_REF = [False]

def low_level_keyboard_proc(nCode, wParam, lParam):
    if nCode == 0 and IS_LOCKED_REF[0]:
        try:
            vkCode = ctypes.cast(lParam, ctypes.POINTER(wintypes.DWORD))[0]
            alt_down = ctypes.windll.user32.GetAsyncKeyState(0x12) & 0x8000
            ctrl_down = ctypes.windll.user32.GetAsyncKeyState(0x11) & 0x8000
            shift_down = ctypes.windll.user32.GetAsyncKeyState(0x10) & 0x8000
            block = False
            if vkCode in (VK_LWIN, VK_RWIN):
                block = True
            if alt_down and vkCode == VK_TAB:
                block = True
            if alt_down and vkCode == VK_F4:
                block = True
            if ctrl_down and vkCode == VK_ESCAPE:
                block = True
            if vkCode == VK_ESCAPE:
                block = True
            if ctrl_down and shift_down and vkCode == VK_DELETE:
                block = True
            if vkCode == 0x5D: # Menu key
                block = True
            if block:
                return 1
        except:
            pass
    try:
        return ctypes.windll.user32.CallNextHookEx(HOOK_HANDLE, nCode, wParam, lParam)
    except:
        return 0

CMP_FUNC = None
HOOK_PROC_PTR = None
try:
    CMP_FUNC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
    HOOK_PROC_PTR = CMP_FUNC(low_level_keyboard_proc)
except:
    pass

def install_hook():
    global HOOK_HANDLE
    try:
        if HOOK_PROC_PTR is None:
            return
        HOOK_HANDLE = ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL, HOOK_PROC_PTR, ctypes.windll.kernel32.GetModuleHandleW(None), 0)
        msg = wintypes.MSG()
        while True:
            ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
    except:
        pass

# ===================== افکت ماتریکس =====================
CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$+-*/=%\"#&_(),.;:?!\\|"

class Drop:
    def __init__(self, x, font, speed_mult):
        self.x = x
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(4, 12) * speed_mult
        self.length = random.randint(8, 28)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.font = font
        self.char_size = max(10, font.get_height())
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
                    color = (180, 255, 180)
                else:
                    r = int(base_color[0] * (1 - i/self.length*0.6))
                    g = int(base_color[1] * (1 - i/self.length*0.2))
                    b = int(base_color[2] * (1 - i/self.length*0.6))
                    color = (r,g,b)
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

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    if WIDTH < 800 or HEIGHT < 600:
        WIDTH, HEIGHT = 1920, 1080

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.DOUBLEBUF)
    pygame.display.set_caption("Matrix Lock v2.1")
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    try:
        font_matrix = pygame.font.SysFont("consolas", config["font_size"], bold=False)
    except:
        font_matrix = pygame.font.Font(None, config["font_size"])
    font_big = pygame.font.SysFont("tahoma", 38, bold=True)
    font_mid = pygame.font.SysFont("tahoma", 20)
    font_small = pygame.font.SysFont("tahoma", 15)

    make_topmost()

    # هوک در ترد جدا (فقط ویندوز)
    try:
        if os.name == "nt":
            t = threading.Thread(target=install_hook, daemon=True)
            t.start()
    except:
        pass

    cols = max(1, WIDTH // (config["font_size"] + 2))
    drops = [Drop(i*(config["font_size"]+2), font_matrix, config["matrix_speed"]) for i in range(cols)]

    locked = True
    if not config["password_hash"]:
        config["password_hash"] = hash_password("1234")
        save_config(config)

    input_pw = ""
    message = ""
    msg_color = (255, 255, 100)
    msg_time = 0
    lock_start_time = time.time()
    show_box_target = True  # هدف نمایش
    box_alpha = 255  # برای Fade نرم 0-255
    FADE_SPEED = 18  # سرعت محو شدن

    # برای تغییر رمز داخل برنامه (F2)
    changing_pw = False
    new_pw = ""
    new_pw2 = ""
    pw_step = 0 # 0=رمز جدید, 1=تکرار

    running = True

    def draw_lock_ui(surf, alpha=255):
        """رسم جعبه قفل با آلفا برای Fade"""
        if alpha <= 0:
            return
        box_w, box_h = 520, 340
        box_x = (WIDTH - box_w)//2
        box_y = (HEIGHT - box_h)//2

        # سطح شیشه‌ای با آلفا
        overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        a = int(185 * alpha / 255)
        overlay.fill((0, 20, 0, a))
        pygame.draw.rect(overlay, (0, 255, 70), (0,0,box_w,box_h), 2, border_radius=18)
        # اعمال آلفا کلی
        overlay.set_alpha(alpha)
        surf.blit(overlay, (box_x, box_y))

        # برای اینکه متن هم fade شود، یک سطح موقت میسازیم
        # فعلا متن را مستقیم با آلفا کم میکشیم
        def blit_alpha(text_surf, pos):
            text_surf.set_alpha(alpha)
            surf.blit(text_surf, pos)

        title = font_big.render("🔒  سیستم قفل است", True, (0,255,120))
        title.set_alpha(alpha)
        surf.blit(title, (box_x + (box_w - title.get_width())//2, box_y + 22))

        sub = font_mid.render("رمز را وارد کنید و Enter بزنید", True, (180,255,180))
        sub.set_alpha(alpha)
        surf.blit(sub, (box_x + (box_w - sub.get_width())//2, box_y + 80))

        now = datetime.now().strftime("%H:%M:%S  -  %Y/%m/%d")
        time_txt = font_mid.render(now, True, (0,255,70))
        time_txt.set_alpha(alpha)
        surf.blit(time_txt, (box_x + (box_w - time_txt.get_width())//2, box_y + 112))

        field_y = box_y + 155
        field_rect = pygame.Rect(box_x+40, field_y, box_w-80, 48)
        # فیلد با آلفا
        field_surf = pygame.Surface((field_rect.width, field_rect.height), pygame.SRCALPHA)
        field_surf.fill((0,0,0, int(220*alpha/255)))
        pygame.draw.rect(field_surf, (0,255,70), (0,0,field_rect.width, field_rect.height), 2, border_radius=10)
        field_surf.set_alpha(alpha)
        surf.blit(field_surf, (field_rect.x, field_rect.y))

        dots = "●" * len(input_pw)
        if dots == "":
            hint = font_small.render("رمز عبور...", True, (100,180,100))
            hint.set_alpha(alpha)
            surf.blit(hint, (field_rect.x+14, field_rect.y+14))
        else:
            txt = font_mid.render(dots, True, (255,255,255))
            txt.set_alpha(alpha)
            surf.blit(txt, (field_rect.x+14, field_rect.y+10))
            if int(time.time()*2) % 2 == 0:
                cx = field_rect.x+14+txt.get_width()+4
                pygame.draw.line(surf, (0,255,70), (cx, field_rect.y+10), (cx, field_rect.y+34), 2)

        if message and time.time()-msg_time < 3:
            mtxt = font_small.render(message, True, msg_color)
            mtxt.set_alpha(alpha)
            surf.blit(mtxt, (box_x + (box_w - mtxt.get_width())//2, field_y+60))

        help1 = font_small.render("Esc پاک کردن  •  Alt+F4 و Win مسدود", True, (120,200,120))
        help1.set_alpha(alpha)
        surf.blit(help1, (box_x + (box_w - help1.get_width())//2, box_y + box_h - 52))
        help2 = font_small.render("Ctrl+Shift+L قفل دستی | Enter تایید", True, (90,170,90))
        help2.set_alpha(alpha)
        surf.blit(help2, (box_x + (box_w - help2.get_width())//2, box_y + box_h - 28))

        warn = font_small.render("Ctrl+Alt+Del توسط ویندوز مسدود نمیشود", True, (200,200,100))
        warn.set_alpha(int(alpha*0.9))
        surf.blit(warn, ((WIDTH - warn.get_width())//2, HEIGHT - 40))

    while running:
        dt = clock.tick(50)
        IS_LOCKED_REF[0] = locked

        # قفل خودکار
        if not locked and not changing_pw and config["idle_timeout"] > 0:
            if get_idle_duration() >= config["idle_timeout"]:
                locked = True
                show_box_target = True
                lock_start_time = time.time()
                input_pw = ""
                message = "قفل خودکار فعال شد"
                msg_color = (0,255,120)
                msg_time = time.time()
                pygame.mouse.set_visible(False)
                make_topmost()

        # منطق محو شدن - Fade
        if locked:
            elapsed = time.time() - lock_start_time
            if elapsed > config["hide_timeout"] and config["hide_timeout"] > 0 and input_pw == "":
                # هیچ ورودی نیست -> هدف محو شدن
                try:
                    keys = pygame.key.get_pressed()
                    any_pressed = any(keys)
                except:
                    any_pressed = False
                if not any_pressed:
                    show_box_target = False
                else:
                    show_box_target = True
                    lock_start_time = time.time()
            else:
                show_box_target = True

            # انیمیشن نرم
            if show_box_target:
                box_alpha = min(255, box_alpha + FADE_SPEED)
            else:
                box_alpha = max(0, box_alpha - FADE_SPEED)
        else:
            box_alpha = 255

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if locked:
                    message = "در حالت قفل نمیتوان بست! رمز را وارد کنید"
                    msg_color = (255,80,80)
                    msg_time = time.time()
                    make_topmost()
                else:
                    running = False

            elif event.type == pygame.KEYDOWN:
                # میانبر قفل دستی
                mods = pygame.key.get_mods()
                if event.key == pygame.K_l and (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT):
                    if not locked and not changing_pw:
                        locked = True
                        show_box_target = True
                        box_alpha = 0
                        lock_start_time = time.time()
                        input_pw = ""
                        pygame.mouse.set_visible(False)
                        message = "قفل دستی فعال شد"
                        msg_color = (0,255,120)
                        msg_time = time.time()
                    continue

                # حالت تغییر رمز (وقتی باز است + F2)
                if changing_pw:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if pw_step == 0:
                            if len(new_pw) < 4:
                                message = "رمز حداقل 4 کاراکتر!"
                                msg_color = (255,80,80)
                                msg_time = time.time()
                                new_pw = ""
                            else:
                                pw_step = 1
                                new_pw2 = ""
                                message = "تکرار رمز را وارد کنید + Enter"
                                msg_color = (100,200,255)
                                msg_time = time.time()
                        else:
                            if new_pw != new_pw2:
                                message = "تکرار اشتباه! دوباره"
                                msg_color = (255,80,80)
                                msg_time = time.time()
                                pw_step = 0
                                new_pw = ""
                                new_pw2 = ""
                            else:
                                config["password_hash"] = hash_password(new_pw)
                                save_config(config)
                                changing_pw = False
                                new_pw = ""
                                new_pw2 = ""
                                message = "✅ رمز با موفقیت تغییر کرد!"
                                msg_color = (0,255,120)
                                msg_time = time.time()
                    elif event.key == pygame.K_ESCAPE:
                        changing_pw = False
                        new_pw = ""
                        new_pw2 = ""
                        message = "لغو شد"
                        msg_color = (200,200,100)
                        msg_time = time.time()
                    elif event.key == pygame.K_BACKSPACE:
                        if pw_step == 0:
                            new_pw = new_pw[:-1]
                        else:
                            new_pw2 = new_pw2[:-1]
                    else:
                        if event.unicode and len(event.unicode)==1 and ord(event.unicode) >= 32:
                            if pw_step == 0 and len(new_pw) < 32:
                                new_pw += event.unicode
                            elif pw_step == 1 and len(new_pw2) < 32:
                                new_pw2 += event.unicode
                    continue

                if not locked:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_F2:
                        changing_pw = True
                        pw_step = 0
                        new_pw = ""
                        new_pw2 = ""
                        message = "رمز جدید را وارد کنید + Enter"
                        msg_color = (100,200,255)
                        msg_time = time.time()
                    continue

                # در حالت قفل: ورودی رمز
                show_box_target = True
                lock_start_time = time.time()
                # اگر الفای کمه، سریع بیار بالا
                if box_alpha < 100:
                    box_alpha = 100
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if hash_password(input_pw) == config["password_hash"]:
                        locked = False
                        input_pw = ""
                        message = ""
                        box_alpha = 255
                        pygame.mouse.set_visible(True)
                    else:
                        message = "❌ رمز نادرست!"
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
                    if event.unicode and len(input_pw) < 32 and ord(event.unicode) >= 32:
                        input_pw += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if locked:
                    show_box_target = True
                    lock_start_time = time.time()
                    box_alpha = min(255, box_alpha+80)
                    make_topmost()
            elif event.type == pygame.MOUSEMOTION:
                if locked and box_alpha < 50:
                    show_box_target = True
                    lock_start_time = time.time()

        # نگه داشتن TOPMOST
        if locked and int(time.time()*3) % 3 == 0:
            try:
                if os.name == "nt":
                    hwnd = pygame.display.get_wm_info()["window"]
                    if ctypes.windll.user32.GetForegroundWindow() != hwnd:
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0,0,0,0, 0x0001|0x0002|0x0010)
            except:
                pass

        # رندر
        screen.fill((0,0,0))
        for d in drops:
            d.update()
            d.draw(screen, tuple(config["matrix_color"]))

        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,70))
        screen.blit(dim, (0,0))

        if locked:
            if box_alpha > 0:
                draw_lock_ui(screen, alpha=box_alpha)
            else:
                cover = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                cover.fill((0,0,0,190))
                screen.blit(cover, (0,0))
                wake = font_mid.render("برای بیداری یک کلید بزنید یا موس را تکان دهید...", True, (0,255,70))
                screen.blit(wake, ((WIDTH-wake.get_width())//2, HEIGHT//2))
                hint2 = font_small.render(f"محو خودکار بعد {config['hide_timeout']} ثانیه", True, (90,170,90))
                screen.blit(hint2, ((WIDTH-hint2.get_width())//2, HEIGHT//2+30))
        else:
            # داشبورد باز
            if changing_pw:
                box_w, box_h = 520, 300
                box_x = (WIDTH - box_w)//2
                box_y = (HEIGHT - box_h)//2
                overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                overlay.fill((0, 20, 30, 190))
                pygame.draw.rect(overlay, (70,180,255), (0,0,box_w,box_h), 2, border_radius=18)
                screen.blit(overlay, (box_x, box_y))
                ttitle = "تغییر رمز - مرحله 1: رمز جدید" if pw_step==0 else "مرحله 2: تکرار رمز"
                txt = font_mid.render(ttitle, True, (100,200,255))
                screen.blit(txt, (box_x+(box_w-txt.get_width())//2, box_y+30))
                field = pygame.Rect(box_x+40, box_y+90, box_w-80, 48)
                pygame.draw.rect(screen, (0,0,0), field, border_radius=10)
                pygame.draw.rect(screen, (70,180,255), field, 2, border_radius=10)
                cur = new_pw if pw_step==0 else new_pw2
                dots = "●"*len(cur)
                if dots:
                    t = font_mid.render(dots, True, (255,255,255))
                    screen.blit(t, (field.x+14, field.y+10))
                else:
                    h = font_small.render("...", True, (100,150,180))
                    screen.blit(h, (field.x+14, field.y+14))
                if message and time.time()-msg_time < 4:
                    mtxt = font_small.render(message, True, msg_color)
                    screen.blit(mtxt, (box_x+(box_w-mtxt.get_width())//2, box_y+155))
                help_text = font_small.render("Enter تایید  •  Esc لغو", True, (120,180,200))
                screen.blit(help_text, (box_x+(box_w-help_text.get_width())//2, box_y+box_h-30))
            else:
                panel = pygame.Surface((580, 240), pygame.SRCALPHA)
                panel.fill((0,20,0,160))
                pygame.draw.rect(panel, (0,255,70), (0,0,580,240), 2, border_radius=16)
                screen.blit(panel, ((WIDTH-580)//2, (HEIGHT-240)//2))
                t1 = font_big.render("✅  سیستم باز است", True, (0,255,120))
                screen.blit(t1, ((WIDTH - t1.get_width())//2, HEIGHT//2 - 60))
                t2 = font_mid.render("Ctrl+Shift+L قفل دستی  •  F2 تغییر رمز", True, (180,255,180))
                screen.blit(t2, ((WIDTH - t2.get_width())//2, HEIGHT//2 + 5))
                t3 = font_small.render(f"قفل خودکار: {config['idle_timeout']}s  |  محو: {config['hide_timeout']}s  |  رمز در config.json", True, (120,200,120))
                screen.blit(t3, ((WIDTH - t3.get_width())//2, HEIGHT//2 + 45))
                t4 = font_small.render("ESC خروج", True, (90,170,90))
                screen.blit(t4, ((WIDTH - t4.get_width())//2, HEIGHT//2 + 75))

        wm = font_small.render("Matrix Lock v2.1  |  github.com/masternewo/matrix-lock", True, (0,180,70))
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
