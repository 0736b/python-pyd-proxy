import sys
import time
import types
import ctypes
import threading

# 'xxxxx' is the 'brain.cp310-win_amd64.pyd' which is the original
# but re-named the exported function name from 'PyInit_brain' to 'PyInit_xxxxx' using 'exported_renamer.py' or tool like 'CFF Explorer'
# so we can import the original 'brain.cp310-win_amd64.pyd' to proxying like this.

import xxxxx

# since we change the exported function name, the 'import brain' in 'main.py' will load our 'brain.py' instead of original pyd
# then the class 'ProxyModule' will exposes everything in 'xxxxx' (original pyd) and when 'main.py' call function in 'brain' it will proxy to 'xxxxx'
# now we can create wrapper to intercept/modify function call of original pyd


original = xxxxx


call_count = 0


def close_info(window_title):
    time.sleep(2)
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd:
        ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)


def show_info(name, attr, returned, auto_close=True):
    global call_count
    WS_EX_TOPMOST = 0x40000
    win_title = f"{call_count}: {name}"
    msg = f"{attr}\nreturned: {returned}"
    threading.Thread(
        target=lambda: ctypes.windll.user32.MessageBoxExW(
            None, msg, win_title, WS_EX_TOPMOST, 0
        )
    ).start()
    if auto_close:
        threading.Thread(target=close_info, args=(win_title,)).start()


class ProxyModule:

    def __init__(self, original):
        self._original = original

    def __getattr__(self, name):
        attr = getattr(self._original, name, None)

        # checking name, type, ... to find your target_function call
        print(f"name: {name}")
        print(f"attr: {attr}")
        print(f"type of attr: {type(attr)}")

        # wrapping target_function to see args and returned value, you can modify the return value too.
        if name == "thinking_number" or name == "select_number":

            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)

                # since assuming main.py to be main.exe build by pyinstaller with no-console, I choose the way to show infomation by MessageBox
                global call_count
                args_msg = f"args: {args}"
                if name == "select_number":
                    show_info(name, args_msg, result, auto_close=False)
                else:
                    show_info(name, args_msg, result, auto_close=True)
                call_count += 1

                return result

            return wrapper

        return attr


proxy_brain = ProxyModule(original)

proxy_brain.__spec__.name = __name__

sys.modules[__name__] = proxy_brain
