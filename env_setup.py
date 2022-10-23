
import platform
import sys

# --------------------------------------------------------
# Keyboard input handler
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
    SYSTEM_INFO['OS'] = platform.system()
    return SYSTEM_INFO