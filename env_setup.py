
import platform
import sys, tty, termios

ESC = chr(27)
SPACE = chr(32)
BACKSPACE = chr(127)
TAB = chr(9)

# --------------------------------------------------------
# Keyboard input handler
# https://docs.python.org/zh-cn/3.7/library/termios.html
# --------------------------------------------------------
s = ['12','13','23','123','45','25']

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class _GetchUnix:
    
    def __init__(self) -> None:
        
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
    
    def getchar(self):
        
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN,self.old_settings)
        return ch
    
    
    
# print("try to input something: ",end='')
# sys.stdout.flush()


def f(ch):
    global show_str
    if ch == ESC:
        pass
        # sys.stdout.write("Esc pressed")
    elif ch == SPACE:
        show_str += ' '
        # sys.stdout.write("space pressed")
    elif ch == TAB:
        show_str += '    '
        # sys.stdout.write("Tab pressed")
    elif ch == BACKSPACE:
        # print("detected backspace!!")
        # sys.stdout.write("\b")
        # show_str = show_str[:-1]
        ch = '\b \b'
    elif ch == 'q':
        # sys.stdout.write("break")
        # sys.stdout.flush()
        return 1
    else:
        # sys.stdout.write(ch)
        show_str += ch
    return ch
    # sys.stdout.flush()

# a = _GetchUnix()
# print(a.getchar())
# while True:
#     a = _GetchUnix()
#     # a = _GetchWindows()
#     ch = f(a())
#     if ch == 1:
#         break

#     sys.stdout.write('\033[1;30;47m'+ch)
#     sys.stdout.flush()


# --------------------------------------------------------
# OS & package manager information
# --------------------------------------------------------
def check_system_info():
    SYSTEM_INFO = {}
    SYSTEM_INFO['machine'] = platform.machine()
    SYSTEM_INFO['network'] = platform.node()
    SYSTEM_INFO['processor'] = platform.processor()
    SYSTEM_INFO['release'] = platform.release()
    SYSTEM_INFO['Type'] = platform.system()
    SYSTEM_INFO['OS'] = platform.platform()
    SYSTEM_INFO['version'] = platform.version()
    SYSTEM_INFO['bit'] = platform.architecture()
    SYSTEM_INFO['python'] = platform.python_version()
    for key,value in SYSTEM_INFO.items():
        print(f"{key}: {value}")