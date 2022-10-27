
import argparse
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from env_setup import *
from script import ScriptParser
from keyboardhandler.keyinput import KeyInput
s = ['1','12','13','23','24','25','15','34','35']

# --------------------------------------------------------
# global variable
# --------------------------------------------------------
word = ''                     # input word
mode = INPUT_MODE             # [INPUT_MODE,SELECT_MODE,DISPLAY_MODE,'RUN'] (see more info in env_setup.py)
select_item = -1              # selected item in SELECT_MODE
display_item = -1             # displayed item in DISPLAY_MODE
all_scripts = {}              # all scripts from ./scripts
keyboard = KeyInput()         # get keyboard input
# --------------------------------------------------------

def main(args):

    # if args.upgrade:
    #     upgrade()
    # if args.g:
    #     set_global()
    
    script = ScriptParser()
    script.environment_check()

    conda_env_name = script.system_info['Conda']['EnvName'] if script.use_conda else ''
    commandline_prompt = f"[b {CMD_PROMPT_COLOR}]({conda_env_name}){CMD_PROMPT}: "
    
    console = Console()
    console.print(Panel(f"[b]{TITLE_NAME}[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal",style=f"on {TITLE_COLOR}"),justify=TITLE_POSITION)
    
    with Live(Panel(commandline_prompt),auto_refresh=False) as input:
        
        while True:
            input.update(input_handler(commandline_prompt))
            input.refresh()

# def upgrade(url):
#     pass

# def set_global():
#     pass


def input_handler(commandline_prompt):
    global word, mode, select_item
    with keyboard as k:
        key = k.get_input()
    if mode == INPUT_MODE and key in NORMAL_CHAR:
        word += key
    elif key in FUNCTION_CHAR:
        function_handler(key)
    else :
        # unsupported keyboard input
        pass
    pannel = Panel(commandline_prompt + f"{word}")
    results = search_result()
    column = Columns([Panel(r,padding=ITEM_PADDING) for r in results])
    
    if mode == SELECT_MODE:
        result_length = len(results)
        if result_length != 0:
            select_item = (select_item+result_length)%result_length
            column.renderables[select_item].style = f"on {ITEM_COLOR}"
    return Group(pannel,column)

def search_result():
    global s    
    result = []
    for i in s:
        if word in i:
            result.append(i)

    return result

def function_handler(key):
    global word, mode, select_item,display_item
    if key == 'ESC':
        # back to the last mode
        if mode == INPUT_MODE:
            # exit program
            exit(0)
        elif mode == SELECT_MODE:
            mode = INPUT_MODE
            select_item = -1
        elif mode == DISPLAY_MODE:
            mode = SELECT_MODE
            select_item = 0
        else:
            mode = DISPLAY_MODE
            
    elif key == 'ENTER' or key == ' ':
        if mode == INPUT_MODE:
            mode = SELECT_MODE
            select_item = 0
        elif mode == SELECT_MODE:
            mode = DISPLAY_MODE
            select_item = -1
            display_item = 0
        elif mode == DISPLAY_MODE:
            mode = RUN_MODE
            display_item = -1
        elif mode == RUN_MODE:
            # run!
            pass
        
    elif key == 'BACKSPACE':
        if mode == INPUT_MODE:
            # delete the last character
            word = word[:-1]
    elif key == 'TAB' or key == 'KEY_RIGHT':
        # next item
        if mode == SELECT_MODE:
            select_item += 1
        elif mode == DISPLAY_MODE:
            display_item += 1
    elif key == 'KEY_LEFT':
        # last item
        if mode == SELECT_MODE:
            select_item -= 1
    elif key == 'KEY_UP':
        if mode == SELECT_MODE:
            mode = INPUT_MODE
            select_item = -1
        elif mode == DISPLAY_MODE:
            display_item -= 1
    elif key == 'KEY_DOWN':
        if mode == DISPLAY_MODE:
            display_item += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)