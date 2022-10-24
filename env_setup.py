
import platform


# --------------------------------------------------------
# Keyboard input handler
# https://docs.python.org/zh-cn/3.7/library/termios.html
# --------------------------------------------------------
s = []
class _GetchUnix:
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return self.f(ch)
        # return ch
    
    def f(self,ch):
        result = []
        for i in s:
            if ch in i:
                result.append(i)
        return result


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