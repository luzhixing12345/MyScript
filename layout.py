

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.console import Group
from rich import box
from script import ScriptParser
from config import *

def make_layout() -> Layout:
    # display layout
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=DISPLAY_LAYOUT_HEADER_SIZE),
        Layout(name="main", ratio=DISPLAY_LAYOUT_MAIN_RATIO),
    )
    layout["main"].split_row(
        Layout(name="side",size=None),
        Layout(name="body",ratio=DISPLAY_LAYOUT_BODY_RATIO, minimum_size=DISPLAY_LAYOUT_BODY_MINSIZE),
    )
    layout["side"].split(Layout(name="md-doc"), Layout(name="code"))
    return layout

def update_layout(layout:Layout, script:ScriptParser, active_position:str, index:int):
    
    active_style = {
        'HEADER': 'none',
        'MD-DOC': 'none',
        'CODE': 'none'
    }
    active_style[active_position] = DISPLAY_ACTIVE_STYLE
    header_content = '[b]'+script.script['name']+'[/b]'
    
    if script.script['type'] == 'INSTALL' and active_position == HEADER:
        # Enter in header should callback script.execute() to INSTALL
        header_content += "  [ENTER TO INSTALL]"
        
    elif script.script['type'] == 'NOTE':
        # TODO DISPLAY
        pass
    
    layout['header'].update(Panel(header_content,style=active_style['HEADER']))
    layout['md-doc'].update(Panel('[b]md-doc[/b]',style=active_style['MD-DOC']))
    layout['code'].update(Panel('[b]code[/b]',style=active_style['CODE']))

    if active_position == HEADER:
    
        script_info = Table.grid(padding=DISPLAY_INFO_TABLE_PADDING)
        script_info.add_column(style=DISPLAY_INFO_COLOR, justify=DISPLAY_INFO_JUSTIFY)
        script_info.add_column(no_wrap=True)
        
        # add script info
        script_info.add_row("repository",create_link(script.script['repository']))
        for description, url in script.script['document'].items():
            script_info.add_row(description,create_link(url))

        body = Panel(
            Align.center(
                Group("\n", Align.center(script_info)),
                vertical="middle",
            ),
            box=box.ROUNDED,
            padding=DISPLAY_INFO_PANEL_PADDING,
            title="[b red]Introduction for "+script.script['name'],
        )
    elif active_position == MD_DOC or active_position == CODE:
        render_number = len(script.script['usage'][active_position.lower()])
        index = (index+render_number)%render_number
        body = Panel(
                script.script['usage'][active_position.lower()][index]['render'],
                title="[b red] "+script.script['usage'][active_position.lower()][index]['path']+f" <{index+1}/{render_number}>"
            )
    
    layout['body'].update(body)
    
def create_link(url):
    return f"[u {DISPLAY_LINK_COLOR} link={url}]{url}"
