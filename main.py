
import argparse
from env_setup import BACKSPACE, ESC, _GetchUnix
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
import time
VERSION = "0.0.1"
keyboard =  _GetchUnix()

s = ['1','12','13','23','24','25','15','34','35']
word = ''
input_clock = 0
def main(args):

    # if args.upgrade:
    #     upgrade()
    # if args.g:
    #     set_global()
    console = Console()
    console.print(Panel(f"[b]MyScript[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal",style="on blue"),justify='center')
    
    
    with Live(Panel(f"[b cyan][MYSCRIPT]: "),auto_refresh=False) as input:
        
        while True:
            input.update(main_input())
            input.refresh()

# def upgrade(url):
#     pass

# def set_global():
#     pass


def main_input():
    global word,input_clock
    key = keyboard.getchar()
    if key == BACKSPACE:
        word = word[:-1]
    elif key == 'WAIT':
        wait_signal = '|' if input_clock else ''
        input_clock = abs(input_clock-1)
        word+=wait_signal
        time.sleep(0.5)
    else:
        word += key
    
    pannel = Panel(f"[b cyan][MYSCRIPT]: {word}")
    if len(word)!=0 and word[-1]=='|':
        word = word[:-1]
    column = handle_search()
    return Group(pannel,column)

def handle_search():
    global s
    result = []
    for i in s:
        if word in i:
            result.append(i)

    return Columns([Panel(r) for r in result])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)