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

class ScriptParser:
    # parse json file in to script action
    def __init__(self,root,name) -> None:
        
        self.actions = []
        self.root = root
        self.file_name = name
        self.load(os.path.join(root,name))
        
    def handle_script(self):
        
        # load from json file
        #"usage": {
        #     "code": [
        #         "./example1.py",
        #         "./example2.py"
        #     ],
        #     "md-doc" : [
        #         "./cv.md"
        #     ]
        # }
        for usage_type,example_paths in self.script['usage'].items():
            for i in range(len(example_paths)):
                relative_path = os.path.join(self.root,example_paths[i])
                if usage_type == 'code':
                    render = Syntax.from_path(relative_path)
                else: # md-doc
                    content = ''
                    with open(relative_path,'r') as f:
                        content.join(f.readlines())
                    render = Markdown(content)
                self.script['usage'][usage_type][i] = render
    
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
        
    def execute(self):
        # execute script
        self.parse_action()
        for action in self.actions:
            try:
                os.system(action)
            except Exception as e:
                raise e
        
    def parse_action(self):
        pass
    
    def display(self):
        return f"[b]{self.script['name']}[/b]\n[yellow]{self.script['type']}"


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
        SYSTEM_INFO['PC']['HostIP'] = os.environ['host_ip']
        SYSTEM_INFO['PC']['Processor'] = platform.processor()
        SYSTEM_INFO['PC']['Release'] = platform.release()
        SYSTEM_INFO['OS']['Type'] = platform.system()
        SYSTEM_INFO['OS']['Infomation'] = platform.platform()
        SYSTEM_INFO['OS']['Version'] = platform.version()
        SYSTEM_INFO['OS']['Bit'] = platform.architecture()
        SYSTEM_INFO['OS']['Home'] = os.environ['HOME']
        SYSTEM_INFO['OS']['HostType'] = os.environ['HOSTTYPE']
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
        