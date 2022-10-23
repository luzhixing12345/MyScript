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
LANGUAGE = ['python','nodejs','java','go','rust']
PACKAGE_MANAGER = {
    'python': ['pip','conda'],
    'nodejs': ['npm'],
    'java': ['maven'],
    'go': ['gomod'],
    'rust': ['cargo']
}


# --------------------------------------------------------
# Integrate
# --------------------------------------------------------

def main():
    print(check_system_info())
    Category = {}
    for root,dirs,files in os.walk(CONFIGURATION_FOLDER,topdown=False):
        # print("@@@",root,dirs,files)
        for name in files:
            # print(root,name)
            process_json(os.path.join(root, name))
    

def process_json(path):
    print(path)
    with open(path,'r') as f:
        return json.load(f)




if __name__ == "__main__":
    main()