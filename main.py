
import argparse
import threading
import os
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from config import *
from script import ScriptParser,EnvironmentInfo
from keyboardhandler.keyinput import KeyInput
s = ['1','12','13','23','24','25','15','34','35']

# --------------------------------------------------------
# global variable
# --------------------------------------------------------
word = ''                     # input word
history_words = []            # search history
history_word_pointer = -1
mode = INPUT_MODE             # [INPUT_MODE,SELECT_MODE,DISPLAY_MODE,'RUN'] (see more info in env_setup.py)
select_item = -1              # selected item in SELECT_MODE
display_item = -1             # displayed item in DISPLAY_MODE
all_scripts = []              # all scripts from ./scripts
keyboard = KeyInput()         # get keyboard input
# --------------------------------------------------------

def load_scripts():
    global all_scripts
    for root,_,files in os.walk(SCRIPTS_POSITION,topdown=False):
        for name in files:
            if not name.endswith('.json'):
                continue
            script = ScriptParser(root,name)
            all_scripts.append(script)
    # print("scripts loaded")

def main(args):

    # if args.upgrade:
    #     upgrade()
    # if args.g:
    #     set_global()
    
    script_loading = threading.Thread(target=load_scripts)
    script_loading.start()
    
    system_info = EnvironmentInfo()
    # system_info.info()
    # conda_env_name = system_info.conda_name if system_info.use_conda else ''
    
    commandline_prompt = f"[b {CMD_PROMPT_COLOR}]{CMD_PROMPT}: "
    
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
    global all_scripts,word
    result = []
    if word == '':
        return result
    for script in all_scripts:
        script:ScriptParser
        for keyword in script.script['keywords']:
            if word in keyword:
                result.append(script.display())
                break

    return result

def function_handler(key):
    global word, mode, select_item,display_item,history_words,history_word_pointer
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
            history_words.append(word)
            history_word_pointer = len(history_words)-1
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
        if mode == INPUT_MODE:
            if history_word_pointer >= 1:
                history_word_pointer -= 1
                word = history_words[history_word_pointer]
                
        if mode == SELECT_MODE:
            mode = INPUT_MODE
            if history_word_pointer != 0:
                history_word_pointer -= 1
                word = history_words[history_word_pointer]
            select_item = -1
        elif mode == DISPLAY_MODE:
            display_item -= 1
    elif key == 'KEY_DOWN':
        if mode == INPUT_MODE:
            if history_word_pointer != len(history_words)-1:
                history_word_pointer += 1
                word = history_words[history_word_pointer]

        if mode == SELECT_MODE:
            mode = INPUT_MODE
            if history_word_pointer != len(history_words)-1:
                history_word_pointer += 1
                word = history_words[history_word_pointer]   
            select_item = -1
            
        if mode == DISPLAY_MODE:
            display_item += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)