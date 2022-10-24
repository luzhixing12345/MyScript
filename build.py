'''
*Copyright (c) 2022 All rights reserved
*@description: integrate all files into Myscript.py
*@author: Zhixing Lu
*@date: 2022-10-23
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
'''

import json
import os

from env_setup import check_system_info

# --------------------------------------------------------
# Basic configuration
# --------------------------------------------------------

SCRIPT_NAME = 'Myscript.py'
CONFIGURATION_FOLDER = 'configuration'
Content = {}

# --------------------------------------------------------
# Integrate
# --------------------------------------------------------

def main():
    check_system_info()
    for root,_,files in os.walk(CONFIGURATION_FOLDER,topdown=False):
        for name in files:
            process_json(os.path.join(root, name))
    
    print(Content)

def process_json(path:str):
    category = path.split(os.sep)[-2]
    name = path.split(os.sep)[-1][:-5] # -5 for .json
    with open(path,'r') as f:
        Content[category][name] = json.load(f)




if __name__ == "__main__":
    main()