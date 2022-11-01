'''
*Copyright (c) 2022 All rights reserved
*@description: parse json file in to script action
*@author: Zhixing Lu
*@date: 2022-10-26
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
'''
import os
import json
import platform
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from config import DISPLAY_CODE_BACKGROUND, DISPLAY_CODE_THEME, DISPLAY_SHOW_LINE_NUMBER, SELECT_ITEM_LANGUAGE_COLOR



class ScriptParser:
    # parse json file in to script action
    def __init__(self,root,name) -> None:
        self.root = root
        self.file_name = name
        self.md_contents = []
        
        self.load(os.path.join(root,name))
        
    def handle_script(self):
        if 'usage' not in self.script.keys():
            return
        
        for usage_type,example_paths in self.script['usage'].items():
            for i in range(len(example_paths)):
                path = example_paths[i]
                relative_path = os.path.join(self.root,path)
                self.script['usage'][usage_type][i] = {}
                
                # render by rich
                if usage_type == 'code':
                    render = Syntax.from_path(
                                relative_path,
                                line_numbers=DISPLAY_SHOW_LINE_NUMBER,
                                theme=DISPLAY_CODE_THEME,
                                background_color=DISPLAY_CODE_BACKGROUND,
                                word_wrap = True,
                                indent_guides = True
                            )
                elif usage_type == 'md-doc':
                    with open(relative_path,'r') as f:
                        # only collect keyword in markdown file instead of code
                        content = f.read()
                        self.md_contents += content.split(' ')
                    render = Markdown(content)
                else:
                    raise "unsupported document type" + usage_type
                self.script['usage'][usage_type][i]['render'] = render
                self.script['usage'][usage_type][i]['path'] = path.split('/')[-1]
    
    def load(self,args):
        # load script from json file or dict
        
        if isinstance(args,str):
            self.file_path = args
            with open(args,'r') as f:
                self.script = json.load(f)
        elif isinstance(args,dict):
            self.script = args
        else:
            raise "unknown argument" + args
        self.handle_script()
        self.check_matched_keywords()
        
    def execute(self):
        # execute script
        for action in self.script['action']:
            try:
                os.system(action)
            except Exception as e:
                raise e
        
    def parse_action(self):
        pass
    
    def check_matched_keywords(self):
        match_field = self.script['keywords'] + [self.script['language']] + [self.script['name']]
        self.matched_keywords = list(set(self.md_contents + match_field))
        
    
    def display(self):
        return f"[{SELECT_ITEM_LANGUAGE_COLOR}]{self.script['name']}[/]\n[b]({self.script['language']})[/b]"


class EnvironmentInfo:
    
    def __init__(self) -> None:
        self.use_conda = False
        self.conda_name = ''
        self.environment_check()

    def environment_check(self):
        SYSTEM_INFO = {'PC':{},'OS':{},'Conda':{}}
        # Basic PC environment
        SYSTEM_INFO['PC']['User'] = os.environ['LOGNAME']
        SYSTEM_INFO['PC']['Machine'] = platform.machine()
        SYSTEM_INFO['PC']['Network'] = platform.node()
        #SYSTEM_INFO['PC']['HostIP'] = os.environ['host_ip']
        SYSTEM_INFO['PC']['Processor'] = platform.processor()
        SYSTEM_INFO['PC']['Release'] = platform.release()
        SYSTEM_INFO['OS']['Type'] = platform.system()
        SYSTEM_INFO['OS']['Infomation'] = platform.platform()
        SYSTEM_INFO['OS']['Version'] = platform.version()
        SYSTEM_INFO['OS']['Bit'] = platform.architecture()
        SYSTEM_INFO['OS']['Home'] = os.environ['HOME']
        #SYSTEM_INFO['OS']['HostType'] = os.environ['HOSTTYPE']
        # Python
        SYSTEM_INFO['Conda']['PythonPath'] = os.environ['_']
        # if pure python without anaconda, recommand conda
        try:
            SYSTEM_INFO['Conda']['EnvName'] = os.environ['CONDA_DEFAULT_ENV']
            SYSTEM_INFO['Conda']['Path'] = os.environ['CONDA_EXE']
            SYSTEM_INFO['Conda']['Prefix'] = os.environ['CONDA_PREFIX']
            SYSTEM_INFO['Conda']['PromptModifier'] = os.environ['CONDA_PROMPT_MODIFIER']
            SYSTEM_INFO['Conda']['SHLVL'] = os.environ['CONDA_SHLVL']
            self.use_conda = True
            self.conda_name = os.environ['CONDA_DEFAULT_ENV']
        except Exception as e:
            # print(e)
            pass
        self.system_info = SYSTEM_INFO
        
        
    def info(self):
        
        for k,_ in self.system_info.items():
            self.table_print(k)
    
    def table_print(self,key_name):
        table = Table()
        table.add_column(key_name,justify='left',style="cyan")
        table.add_column('Info',justify='left')
        
        for key,value in self.system_info[key_name].items():
            table.add_row(key,str(value))
        console = Console()
        console.print(table)
        
