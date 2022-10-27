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

class ScriptParser:
    # parse json file in to script action
    def __init__(self,file_name='') -> None:
        self.use_conda = False
        self.actions = []
        if file_name != '':
            self.load(file_name)
    
    def load(self,args):
        # load script from json file or dict
        
        if isinstance(args,str):
            with open(args,'r') as f:
                self._script = json.load(f)
        elif isinstance(args,dict):
            self.script = args
        else:
            raise "unknown argument" + args
        
    def execute(self):
        # execute script
        self.environment_check()
        self.parse_action()
        for action in self.actions:
            try:
                os.system(action)
            except Exception as e:
                raise e
            
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
        except Exception as e:
            # print(e)
            pass
        self.system_info = SYSTEM_INFO
        # for k,_ in self.system_info.items():
        #     self.table_print(k)
        
    def parse_action(self):
        pass
    
    def table_print(self,key_name):
        
        table = Table()
        table.add_column(key_name,justify='left',style="cyan")
        table.add_column('Info',justify='left')
        
        for key,value in self.system_info[key_name].items():
            table.add_row(key,str(value))
        console = Console()
        console.print(table)
            

def main():
    scripts = []
    for root,_,files in os.walk('./scripts/python/opencv',topdown=False):
        for name in files:
            if not name.endswith('.json'):
                continue
            script = ScriptParser(os.path.join(root, name))
            script.environment_check()
            # scripts.append(script)
    # print(len(scripts))

    
if __name__ == "__main__":
    main()