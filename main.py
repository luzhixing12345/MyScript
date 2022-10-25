
import argparse
import sys
from env_setup import _GetchUnix
from rich.console import Console
from rich.columns import Columns
from rich.prompt import Prompt
from rich.panel import Panel

VERSION = "0.0.1"

def main(args):
    print(args)
    if args.upgrade:
        upgrade()
    if args.g:
        set_global()
    console = Console()
    console.print(Panel(f"[b]MyScript[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal"),justify='center')
    console.print("[b cyan][MYSCRIPT]:",end='')
    while True:
        a = _GetchUnix()
        # a = _GetchWindows()
        ch = a.getchar()
        if ch == 'q':
            break

        sys.stdout.write('\033[1;30;47m'+ch)
        sys.stdout.flush()
def upgrade(url):
    pass

def set_global():
    pass





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)