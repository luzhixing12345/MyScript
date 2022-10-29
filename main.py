
import argparse
import threading
import os
from time import sleep
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from rich.layout import Layout
from config import *
from layout import *
from script import ScriptParser,EnvironmentInfo
from keyboardhandler.keyinput import KeyInput
from typing import List

# --------------------------------------------------------
# global variable
# --------------------------------------------------------
word:str = ''                           # input word
history_words:List[str] = []            # search history
history_word_pointer:int = -1
mode:int = INPUT_MODE                   # [INPUT_MODE,SELECT_MODE,DISPLAY_MODE,'RUN'] (see more info in env_setup.py)
select_item:int = -1                    # selected item in SELECT_MODE
selected_script:ScriptParser = None 
display_item:int = -1                   # displayed item in DISPLAY_MODE
all_scripts:List[ScriptParser] = []     # all scripts from ./scripts
display_active_position:str = HEADER    # active postion in DISPLAY MODE
display_body_item:int = -1
keyboard = KeyInput()                   # get keyboard input
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
    console.clear()
    console.print(Panel(f"[b]{TITLE_NAME}[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal"),justify=TITLE_POSITION)

    with Live(Panel(commandline_prompt,style=f"on {INPUT_ACTIVE_STYLE}"),auto_refresh=False) as live:
        
        while True:
            live.update(input_handler(commandline_prompt))
            live.refresh()

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
        # do not respond to keyboard input
        pass
    
    input_style = f"on {INPUT_ACTIVE_STYLE}" if mode == INPUT_MODE else "none"
    search_part = Panel(commandline_prompt + f"{word}",style=input_style)
    display_part = get_display_part()
    
    if type(display_part) is Layout:
        return display_part
    else:
        return Group(search_part,display_part)

def get_display_part():
    global mode,selected_script,select_item
    global display_active_position,display_body_item
    if mode == INPUT_MODE or mode == SELECT_MODE:
        scripts_result = search_result()
        display_part = Columns([Panel(script.display(),padding=SELECTED_ITEM_PADDING) for script in scripts_result])
        
        # highlight the selected block, filled with color
        if mode == SELECT_MODE:
            result_length = len(scripts_result)
            if result_length != 0:
                select_item = (select_item+result_length)%result_length
                display_part.renderables[select_item].style = f"on {SELECTED_ITEM_COLOR}"
                selected_script = scripts_result[select_item] # get the selected script
            else:
                # no matched result, back to INPUT MODE
                mode = INPUT_MODE
            
    elif mode == DISPLAY_MODE:
        
        display_part = make_layout()
        update_layout(display_part,selected_script,display_active_position,display_body_item)
    
    return display_part




def search_result() -> List[ScriptParser]:
    scripts_result = []
    global all_scripts,word
    if word == '':
        return scripts_result
    search_words = word.split(' ')
    for script in all_scripts:
        script:ScriptParser
        if match_keyword(search_words,script):
            scripts_result.append(script)

    return scripts_result

def match_keyword(search_words,script:ScriptParser):
    
    script_match_field = script.matched_keywords
    for keyword in script_match_field:
        for word in search_words:
            if word in keyword:
                return True

def function_handler(key):
    global word, mode, select_item,display_item,history_words,history_word_pointer
    global display_active_position,display_body_item
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
            display_body_item = -1
        else:
            mode = DISPLAY_MODE
            
    elif key == 'ENTER':
        if mode == INPUT_MODE:
            history_words.append(word)
            history_word_pointer = len(history_words)-1
            mode = SELECT_MODE
            select_item = 0
        elif mode == SELECT_MODE:
            mode = DISPLAY_MODE
            select_item = -1
            display_active_position = HEADER
        elif mode == DISPLAY_MODE:
            if display_active_position == HEADER:
                mode = RUN_MODE
                
        elif mode == RUN_MODE:
            # run!
            pass
        
    elif key == 'BACKSPACE':
        if mode == INPUT_MODE:
            # delete the last character
            word = word[:-1]
    elif key == 'KEY_RIGHT':
        # next item
        if mode == SELECT_MODE:
            select_item += 1
        elif mode == DISPLAY_MODE:
            if display_active_position == MD_DOC or display_active_position == CODE:
                # show the next render
                display_body_item += 1
                
    elif key == 'KEY_LEFT':
        # last item
        if mode == SELECT_MODE:
            select_item -= 1
        elif mode == DISPLAY_MODE:
            if display_active_position == MD_DOC or display_active_position == CODE:
                # show the next render
                display_body_item -= 1
            
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
            
    elif key == 'TAB':
        # only active in DISPLAY MODE
        # change between four HEADER | MD_DOC | CODE | BODY
        if mode == DISPLAY_MODE:
            if display_active_position == HEADER:
                display_active_position = MD_DOC
            elif display_active_position == MD_DOC:
                display_active_position = CODE
            elif display_active_position == CODE:
                display_active_position = HEADER
            else:
                raise "unknown display position"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script for auto environment setup')
    parser.add_argument('--upgrade',action='store_true',help='get the lastest MyScript.py')
    parser.add_argument('-g',action='store_true',help='set MyScript.py a global varable')
    args = parser.parse_args()
    main(args)