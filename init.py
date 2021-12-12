# configuration for MITE
from blessed import Terminal
import time

term = Terminal()

syntax_highlight = True
colour_theme = {
    'tab_selected': term.bold_white_on_cyan,
    'tab_unselected': term.normal,
    'normal_mode_bar': term.bold_white_on_green,
    'insert_mode_bar': term.bold_white_on_purple,
    'command_mode_bar': term.bold_white_on_red,
    'line_number_current': term.bold_orange,
    'line_number_other': term.white,
    'cursor': term.black_on_white,
}
language_bindings = { # 'file_extension': 'language_name'
    'py': 'python',
    'sh': 'bash',
    'md': 'markdown',
    'txt': 'plaintext',
    'html': 'html',
    'css': 'css',
    'js': 'javascript',
    'json': 'json',
    'xml': 'xml',
    'yml': 'yaml',
    'yaml': 'yaml',
    'toml': 'toml',
    'ini': 'ini',
    'sql': 'sql',
    'sqlite': 'sqlite',
    'sqlite3': 'sqlite',
    'db': 'sqlite',
    'db3': 'sqlite',
    'c': 'c',
    'cpp': 'cpp',
    'h': 'cpp',
    'hpp': 'cpp',
    'hxx': 'cpp',
    'h++': 'cpp',
    'cc': 'cpp',
    'cxx': 'cpp',
    'c++': 'cpp',
    'cs': 'csharp',
    'csx': 'csharp',
    'csi': 'csharp',
    'csv': 'csv',
    'java': 'java',
    'jav': 'java',
    'javx': 'java',
    'javs': 'java',
    'jsp': 'jsp',
    'jspx': 'jsp',
    'jspf': 'jsp',
    'jspc': 'jsp',
    'jspa': 'jsp',
    'jspx': 'jsp',
    'kt': 'kotlin',
    'nim': 'nim',
    'vim': 'vim',
    'vimrc': 'vim',
    'vba': 'vba',
    'vb': 'vba',
    'vbs': 'vbs',
    'vbx': 'vbs',
    'vbw': 'vbs',
    'vbproj': 'vbproj',
    'bat': 'batch',
    'cmd': 'batch',
    'lua': 'lua',
    'luau': 'luau',
    'rs': 'rust',
    'krk': 'kuroko',
    'hs': 'haskell',
    'hx': 'haxe',
}

def IDE_init(
            opened_project_path = '',
            opened_project_ls = '',
            mode = '',
            buffer = [],
            current_tab = '',
            current_command = '',
            parse_command = lambda: None,
            write_buffer = lambda: None,
            process_input = lambda: None
        ):
    parse_command(
        'goto column ' + str(len(buffer[0]['content'][0]) + 1) # goto end of line
    )