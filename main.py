
import argparse
import threading
import os
import sys
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from rich.layout import Layout
from rich.text import Text
from config import *
from layout import *
from script import ScriptParser,EnvironmentInfo,Script
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
all_scripts:List[ScriptParser] = []     # all scripts from ./scripts
display_active_position:str = HEADER    # active postion in DISPLAY MODE
display_body_item:int = 0
keyboard = KeyInput()                   # get keyboard input
console = Console()
# --------------------------------------------------------

def load_scripts(script_path:str):
    global all_scripts
    for root,_,files in os.walk(script_path,topdown=False):
        for name in files:
            if not name.endswith('.json'):
                continue
            script = ScriptParser(root,name)
            all_scripts.append(script)
    # print("scripts loaded")

def main(args):
    
    system_info = EnvironmentInfo()
    if args.env:
        # set MyScript to path
        python_path = system_info.system_info['Conda']['PythonPath']
        absolute_path = os.getcwd()
        home_path = system_info.system_info['OS']['Home']
        with open(os.path.join(home_path,'.bashrc'),'a') as f:
            f.write("\nmsp(){ "+python_path+" "+absolute_path+"/main.py $1;}")
        print("finished!")
        print("please run \"source ~/.bashrc\" to activate your environment")
        print("Then you could use \"msg\" to run this program in everywhere")
        return
    
    # parse python path
    if sys.argv[0] == 'main.py' or sys.argv[0] == './main.py':
        scripts_path = SCRIPTS_POSITION
    else:
        scripts_path = '/'
        scripts_path = scripts_path.join(sys.argv[0].split('/')[:-1]) + "/" + SCRIPTS_POSITION
        
    # start a thread for file loading
    script_loading = threading.Thread(target=load_scripts,args=(scripts_path,))
    script_loading.start()
    
    if args.add:
        script = Script()
        script.generate(scripts_path)
        script_loading.join()
        print(f"Successfully create a new script [{script.script_name}]!")
        return
    # system_info.info()
    # conda_env_name = system_info.conda_name if system_info.use_conda else ''
    
    commandline_prompt = f"[b {CMD_PROMPT_COLOR}]{CMD_PROMPT}: "
    
    global console
    console.clear()
    console.print(Panel(f"[b]{TITLE_NAME}[/b] [magenta]v{VERSION}[/]\n\n[dim]script for auto environment setup in the terminal"),justify=TITLE_POSITION)

    with Live(Panel(commandline_prompt+'[blink]|[/blink]',style=f"on {INPUT_ACTIVE_STYLE}"),auto_refresh=False) as live:
        # live.console.print("finish loading")
        while True:
            live.update(input_handler(commandline_prompt))
            live.refresh()

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
    if mode == INPUT_MODE:
        search_part = Panel(commandline_prompt + f"{word}[blink]|[/blink]",style=input_style)
    else:
        search_part = Panel(commandline_prompt + f"{word}",style=input_style)
    display_part = get_display_part()
    
    if type(display_part) is Layout:
        return display_part
    else:
        return Group(search_part,display_part)

def get_display_part():
    global mode,selected_script,select_item,console
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
                # no matched result, ask if need to create new script
                select_item = -1
                return Text(f"No result \'{word}\'found, use \"-a\" to add new script, or ESC to step back",justify='center')
            
    elif mode == DISPLAY_MODE:
        display_part = make_layout()
        update_layout(display_part,selected_script,display_active_position,display_body_item)
    
    elif mode == RUN_MODE:
        with console.screen():
            selected_script.execute()
        mode = DISPLAY_MODE
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
    global word, mode, select_item,history_words,history_word_pointer,console
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
            display_body_item = 0
        else:
            mode = DISPLAY_MODE
            
    elif key == 'ENTER':
        if mode == INPUT_MODE:
            history_words.append(word)
            history_word_pointer = len(history_words)-1
            mode = SELECT_MODE
            select_item = 0
            
        elif mode == SELECT_MODE:
            if select_item == -1: # no result
                return
            mode = DISPLAY_MODE
            select_item = -1
            display_active_position = HEADER
            
        elif mode == DISPLAY_MODE:
            if display_active_position == HEADER:
                mode = RUN_MODE
        
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
            
            
    elif key == 'TAB':
        # only active in DISPLAY MODE
        # change between four HEADER | MD_DOC | CODE | BODY
        # print(display_active_position)
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
    parser.add_argument('-e',"--env",action='store_true',help='set MyScript global to run')
    parser.add_argument('-a',"--add",action='store_true',help='add json config script for MyScript')
    args = parser.parse_args()
    main(args)