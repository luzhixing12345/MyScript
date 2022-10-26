
import argparse
from env_setup import BACKSPACE, CURSOR_BLINKING_SLEEPTIME, CURSOR_BLINKING_SYMBOL, CURSOR_BLINKING_TIMER, VERSION,CMD_PROMPT,CMD_PROMPT_COLOR,_GetchUnix
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
import time
from env_setup import keyboard
s = ['1','12','13','23','24','25','15','34','35']
word = ''
TIMER = 0

def main(args):

    # if args.upgrade:
    #     upgrade()
    # if args.g:
    #     set_global()
    console = Console()
    console.print(Panel(f"[b]MyScript[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal",style="on blue"),justify='center')
    
    
    with Live(Panel(f"[b {CMD_PROMPT_COLOR}]{CMD_PROMPT}: "),auto_refresh=False) as input:
        
        while True:
            input.update(main_input())
            input.refresh()

# def upgrade(url):
#     pass

# def set_global():
#     pass


def main_input():
    global word,TIMER
    blink_signal = False # whether add CURSOR_BLINKING_SYMBOL after word
    key = keyboard.getchar()
    if key == BACKSPACE: # remove last character
        word = word[:-1]
    elif key == 'WAIT':
        # wait for input
        # Simulate cursor blinking
        TIMER += 1
        if TIMER == CURSOR_BLINKING_TIMER:
            word += CURSOR_BLINKING_SYMBOL
            blink_signal = True
            TIMER = 0
        time.sleep(CURSOR_BLINKING_SLEEPTIME)
    else:
        word += key
    
    pannel = Panel(f"[b {CMD_PROMPT_COLOR}]{CMD_PROMPT}: {word}")
    # clear CURSOR_BLINKING_SYMBOL
    if len(word)!=0 and blink_signal:
        word = word[:-1]
    column = search_result()
    return Group(pannel,column)

def search_result():
    global s    
    result = []
    for i in s:
        if word == '':
            break
        if word in i:
            result.append(i)

    return Columns([Panel(r) for r in result])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)