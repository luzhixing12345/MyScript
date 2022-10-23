'''
*Copyright (c) 2022 All rights reserved
*@description: auto Linux environment setup without root
*@author: Zhixing Lu
*@date: 2022-10-23
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
'''










# --------------------------------------------------------
# Keyboard input handler
# --------------------------------------------------------

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
    
a = _GetchUnix()
print(a())