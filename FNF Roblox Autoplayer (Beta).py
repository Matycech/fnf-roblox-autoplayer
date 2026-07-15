import mss
import keyboard
import time
import ctypes
import os
import winsound

# ==========================================
# NASTAVENÍ BOTA
# ==========================================
DIRECTIONS = ['left', 'down', 'up', 'right']
USER_KEYS = {}

TARGET_COLORS = {
    'left':  (194, 75, 153),
    'down':  (0, 255, 255),
    'up':    (18, 250, 5),
    'right': (249, 57, 63)
}
# Pokud bot dlouhé noty pouští moc brzy, zvyš tuto hodnotu (např. na 60-80)
TOLERANCE = 40

calibrated_coords = {}
is_running = False
is_calibrated = False

# Paměť pro dlouhé noty (zda aktuálně klávesu držíme, nebo ne)
key_states = {
    'left': False,
    'down': False,
    'up': False,
    'right': False
}

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def color_match(actual_rgb, target_rgb, tolerance):
    return all(abs(actual_rgb[i] - target_rgb[i]) <= tolerance for i in range(3))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_keys():
    clear_console()
    print("=== NASTAVENÍ KLÁVES ===")
    for direction in DIRECTIONS:
        key = input(f"Klávesa pro směr [{direction.upper()}]: ").strip().lower()
        if key == "":
            key = direction
        USER_KEYS[direction] = key
    print("\nKlávesy uloženy!")
    time.sleep(1)

def print_status():
    clear_console()
    print("=== UNIVERZÁLNÍ FNF BOT ===")
    print("---------------------------")
    for d in DIRECTIONS:
        print(f"  {d.upper()} -> '{USER_KEYS[d]}'")
    print("---------------------------")
    print(f"Stav kalibrace: {'[OK]' if is_calibrated else '[CHYBÍ - Stiskni F6]'}")
    print(f"Stav hraní:     {'[AKTIVNÍ]' if is_running else '[POZASTAVENO]'}")
    print("---------------------------")
    print("[Pravý Shift] -> Spustit / Pozastavit hraní")
    print("[F6]          -> Nová kalibrace souřadnic")
    print("[Q]           -> Úplně vypnout program")
    print("===========================\n")

def calibrate():
    global is_calibrated, is_running
    is_running = False 
    
    # Při nové kalibraci raději pustíme všechny klávesy
    for direction in DIRECTIONS:
        if USER_KEYS and direction in USER_KEYS:
            keyboard.release(USER_KEYS[direction])
            key_states[direction] = False
            
    clear_console()
    print("=== KALIBRACE ZAHÁJENA ===")
    print("Najeď myší na cíl a stiskni MEZERNÍK (Space).")
    
    for direction in DIRECTIONS:
        print(f"\nČekám na směr: [{direction.upper()}] -> Najeď myší a stiskni MEZERNÍK")
        
        while keyboard.is_pressed('space'):
            time.sleep(0.01)
            
        while not keyboard.is_pressed('space'):
            time.sleep(0.01)
            
        x, y = get_mouse_pos()
        calibrated_coords[direction] = {"top": y, "left": x, "width": 1, "height": 1}
        
        winsound.Beep(1000, 150)
        print(f"✅ ÚSPĚŠNĚ ULOŽENO! X={x}, Y={y}")
        
    is_calibrated = True
    print("\nKalibrace úspěšná! Pro start stiskni Pravý Shift.")
    time.sleep(2)
    print_status()

def main():
    global is_running
    setup_keys()
    print_status()
    
    with mss.mss() as sct:
        while True:
            if keyboard.is_pressed('q'):
                # Při vypínání uvolníme všechny klávesy
                for d in DIRECTIONS:
                    keyboard.release(USER_KEYS[d])
                break
                
            if keyboard.is_pressed('f6'):
                calibrate()
                
            if keyboard.is_pressed('right shift'):
                if not is_calibrated:
                    print("Nejdřív kalibruj (F6)!")
                    time.sleep(1)
                    print_status()
                else:
                    is_running = not is_running
                    # Pokud pozastavujeme bota, uvolníme držené klávesy
                    if not is_running:
                        for d in DIRECTIONS:
                            keyboard.release(USER_KEYS[d])
                            key_states[d] = False
                    print_status()
                    time.sleep(0.3)

            if is_running and is_calibrated:
                for direction in DIRECTIONS:
                    monitor = calibrated_coords[direction]
                    screenshot = sct.grab(monitor)
                    actual_color = screenshot.pixel(0, 0)
                    mapped_key = USER_KEYS[direction]
                    
                    # Logika pro dlouhé noty
                    if color_match(actual_color, TARGET_COLORS[direction], TOLERANCE):
                        # Barva detekována - pokud klávesu nedržíme, stiskneme ji
                        if not key_states[direction]:
                            keyboard.press(mapped_key)
                            key_states[direction] = True
                    else:
                        # Barva chybí - pokud klávesu držíme, pustíme ji
                        if key_states[direction]:
                            keyboard.release(mapped_key)
                            key_states[direction] = False

if __name__ == "__main__":
    main()