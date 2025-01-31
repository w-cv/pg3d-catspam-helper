import dxcam
from PIL import Image
from time import time
import pyautogui
import pydirectinput
import win32api
import win32con
import winsound

# Play a beep sound
frequency = 440  # Frequency in Hz (A4)
duration = 20   # Duration in milliseconds
def is_red(color):
    if color[0] > 250 and color[1] < 5 and color[2] < 5:
        return 1
    return 0


pyautogui.PAUSE = 0  # Removes the delay

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
"""while (True):
    PressKey(0x02)
    time.sleep(1)
    ReleaseKey(0x02)
    time.sleep(1)"""
def press_key(hex, delay):
    PressKey(hex)
    pyautogui.sleep(delay)
    ReleaseKey(hex)
# st = time()
# howl of mummy 0.265
# pixel cola refresher has no fixed delay
# terramorphing stone 0.265
# weapon_fixed_delay =    [0,0,0,0.265,0,0] # stores the delay time in second
weapon_fixed_delay =    [0,0,0,0.265,0,0.265] # stores the delay time in second
weapon_receives_delay = [1,1,0,0    ,1,0    ] # 1=true 0=false
weapon_gives_delay =    [1,1,0,0    ,1,0    ] # 1=true 0=false

# for bloody
weapon_order = [5,6,1,4,2] # 1 indexed, the order you spam the weapons
# weapon_order = [5,6,1,4,2] # 1 indexed, the order you spam the weapons
wlen = weapon_order.__len__()

# intermediate weapon is the weapon to spam when delay
intermediate_weapon = 0

if weapon_fixed_delay[2] == 0 and weapon_receives_delay[2] == 0 and weapon_gives_delay[2] == 0: # if melee has no delay
    intermediate_weapon = 3 # use melee as intermediate weapon
else:
    for i in range(6):
        if weapon_fixed_delay[i] == 0 and weapon_receives_delay[i] == 0 and weapon_gives_delay[i] == 0:
            intermediate_weapon = i + 1 # 1-indexed
            break
if intermediate_weapon == 0:
    print("no intermediate weapon")
    exit(-1)

# now we compute if intermediate weapon is needed
# if intermediate weapon is required, 1, else 0
intermediate_list = [0]*wlen # when switched from index 0 to index 1, we see index 1 in this list
for i in range(wlen):
    prei = i - 1 # the index before i
    if prei < 0:
        prei += wlen
    if weapon_gives_delay[weapon_order[prei]-1] == 1 and weapon_receives_delay[weapon_order[i]-1] == 1:
        intermediate_list[i] = 1

print(intermediate_list)

windex = 0 # the index insider array
enable = 0
cheat = 0
camera = dxcam.create()  # returns a DXCamera instance on primary monitor
weapon = 5 # weapon for cheat
while 1: # this is main loop

    if windex == 0:
        prev_windex = wlen - 1 # prev_windex is the previous index of windex
    else:
        prev_windex = windex - 1
    ### we do touchdown gautlet movement
    if win32api.GetAsyncKeyState(0x51) < 0: # if q is pressed
        press_key(4,0.01) # switch to melee
        pyautogui.sleep(0.40)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        pyautogui.sleep(0.65)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        pyautogui.sleep(0.01)
        while win32api.GetAsyncKeyState(0x51) < 0: # if q is pressed
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.65)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)
        # now we should switch to the weapon we are originally holding
        press_key(weapon_order[prev_windex]+1, 0.01) # add 1 is for the key hexcode, i.e. the hex code of button 1 is 2
        print(f"sleep {0.45 + weapon_fixed_delay[weapon_order[prev_windex] - 1]}")
        pyautogui.sleep(0.45 + weapon_fixed_delay[weapon_order[prev_windex] - 1])

    ### this is for enabling the program (maybe considering not using busy waiting...)
    if win32api.GetAsyncKeyState(0xC0) < 0:
        enable = not enable
        print(enable)
        if enable:
            winsound.Beep(440, duration)
            winsound.Beep(466, duration)
        else:
            winsound.Beep(466, duration)
            winsound.Beep(440, duration)
        pyautogui.sleep(0.2)
    ### this is for cheat, it detects red dots
    if win32api.GetAsyncKeyState(0x08) < 0:# detect for cheat
        cheat = not cheat
        print(f"cheat {cheat}")
        if cheat:
            winsound.Beep(880, duration)
            winsound.Beep(932, duration)
        else:
            winsound.Beep(932, duration)
            winsound.Beep(880, duration)
        pyautogui.sleep(0.2)
    ### enable not cheat, we do auto cat spam weapon switch
    if (not cheat) and enable and win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
        ### click to shoot
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        pyautogui.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        pyautogui.sleep(0.01)
        
        
        
        if intermediate_list[windex] == 1:
            ### switch to intermediate weapon
            press_key(intermediate_weapon+1, 0.02) # +1 is for hex code of key
            pyautogui.sleep(0.25)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)


        press_key(weapon_order[windex]+1, 0.01) # add 1 is for the key hexcode, i.e. the hex code of button 1 is 2
        print(f"sleep {0.45 + weapon_fixed_delay[weapon_order[windex] - 1]}")
        pyautogui.sleep(0.45 + weapon_fixed_delay[weapon_order[windex] - 1])
        windex += 1
        windex %= wlen
    elif cheat and enable:
        ### if cheat enable, we detect red dots, or clicked, we fire
        frame = camera.grab()
        if frame is None:
            continue
        pixel_color = frame[539, 960]  # (row, column) order
        pixel_color_ultimatum = frame[539, 987]  # (row, column) order
        pixel_color_terra= frame[546, 981]  # (row, column) order

        if windex == 0:
            prev_windex = wlen - 1 # prev_windex is the previous index of windex, But it is actually the weapon currently holding
        else:
            prev_windex = windex - 1
        cwii = weapon_order[prev_windex] # current_weapon_ingame_index
        # print(cwii)
        # print(f"pixel_color: {pixel_color}")
        # print(f"pixel_color_ultimatum: {pixel_color_ultimatum}")
        # print(f"pixel_color_terra: {pixel_color_terra}")
        should_fire = ((cwii == 2 or cwii == 5 or cwii == 6) and (pixel_color[0] > 250 and pixel_color[1] == 0 and pixel_color[2] == 0)) or \
((cwii == 1) and (pixel_color_ultimatum[0] == 255 and pixel_color_ultimatum[1] == 0 and pixel_color_ultimatum[2] == 0)) or \
((cwii == 4) and (pixel_color_terra[0] == 255 and pixel_color_terra[1] == 0 and pixel_color_terra[2] == 0))
        

        if should_fire or win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)
            
            
            if intermediate_list[windex] == 1:
                ### switch to intermediate weapon
                press_key(intermediate_weapon+1, 0.02) # +1 is for hex code of key
                pyautogui.sleep(0.25)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                pyautogui.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                pyautogui.sleep(0.01)


            press_key(weapon_order[windex]+1, 0.01) # add 1 is for the key hexcode, i.e. the hex code of button 1 is 2
            print(f"sleep {0.45 + weapon_fixed_delay[weapon_order[windex] - 1]}")
            pyautogui.sleep(0.45 + weapon_fixed_delay[weapon_order[windex] - 1])
            windex += 1
            windex %= wlen






            """win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)


            ### switch to melee (press 3)
            press_key(0x04, 0.01)
            pyautogui.sleep(0.25)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)
            ### switch to backup
            press_key(0x03, 0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            pyautogui.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            pyautogui.sleep(0.01)
            if weapon == 5:
                ### switch to backup (press 2)
                press_key(0x03, 0.01)
                pyautogui.sleep(0.1)
                weapon = 2
            elif weapon == 2:
                press_key(0x06, 0.01)
                pyautogui.sleep(0.1)
                weapon = 5"""


# print(time()-st)