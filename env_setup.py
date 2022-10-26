
import platform
import sys, tty, termios
import select
ESC = chr(27)
SPACE = chr(32)
BACKSPACE = chr(127)
TAB = chr(9)
TAB_SPACE = 4
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
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(self.fd)
    
    def getchar(self):
        
        # try:
        
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            ch = sys.stdin.read(1)
            return self.handleinput(ch)
        else:
            return 'WAIT'
    
    def handleinput(self,ch):
        if ch == ESC:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            exit(0)
        elif ch == SPACE:
            return ' '
        elif ch == TAB:
            return ' ' * TAB_SPACE
        else:
            return ch

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