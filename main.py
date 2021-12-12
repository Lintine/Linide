# Linide - LINtine IDE
# Vim-like text editor in Python with Blessed

from blessed import Terminal
import sys
import os

import init as config

term = Terminal()

opened_project_path = None
opened_project_ls = None

mode = 'normal'

buffer = [
    {
        'path': None,
        'content': [[c for c in 'Welcome to Linide - LINtine IDE!'], [c for c in 'Type :help for help.']],
        'cursor': [0, 0],
        'scroll': [0, 0], # offset of the top left corner of the render
        'selection': [[None, None], [None, None]], # coordinates of the selection start and end
    },
] # Dict of nested arrays of lines and characters
current_tab = 0

current_command = ''

if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Linide - LINtine IDE')
        print('Usage: lintine [project_path]')
        print('-h, --help: Show this help message')
        print('project_path: Path to a folder or file to open')
        print('If no project path is given, a new file will be created')
        exit(0)
    else:
        if os.path.isdir(sys.argv[1]):
            print('Opening project...')
            opened_project_path = sys.argv[1]
            opened_project_ls = os.listdir(opened_project_path)
        elif os.path.isfile(sys.argv[1]):
            print('Opening file...')
            with open(sys.argv[1], 'r') as f:
                lines = f.readlines()
                lines = [line.rstrip('\n') for line in lines]
                lines = [line.split() for line in lines]
                buffer = {
                    'path': sys.argv[1],
                    'content': lines,
                    'cursor': [0, 0],
                    'scroll': [0, 0], # offset of the top left corner of the render
                    'selection': [[None, None], [None, None]], # coordinates of the selection start and end
                }
        else:
            print('Invalid path')
            exit(1)

def parse_command(command):
    global buffer, current_tab, mode
    if command.lstrip().rstrip() == '':
        return
    words = command.split(' ')
    if words[0] == 'quit':
        if len(words) > 1 and words[1] == 'save':
            for tab in buffer:
                if tab['path'] != None:
                    with open(tab['path'], 'w') as f:
                        for line in tab['content']:
                            f.write(' '.join(line) + '\n')
        exit(0)
    elif words[0] == 'new':
        buffer.append({
            'path': None,
            'content': [[c for c in 'New file']],
            'cursor': [0, 0],
            'scroll': [0, 0], # offset of the top left corner of the render
            'selection': [[None, None], [None, None]], # coordinates of the selection start and end
        })
        current_tab = len(buffer) - 1
    elif words[0] == 'close':
        if len(words) > 1:
            if words[1] == 'all':
                buffer = [
                    {
                        'path': None,
                        'content': [[c for c in 'Welcome to Linide - LINtine IDE!'], [c for c in 'Type :help for help.']],
                        'cursor': [0, 0],
                        'scroll': [0, 0], # offset of the top left corner of the render
                        'selection': [[None, None], [None, None]], # coordinates of the selection start and end
                    },
                ]
                current_tab = 0
            else:
                try:
                    buffer.pop(int(words[1]) - 1)
                    if current_tab > len(buffer) - 1:
                        current_tab = len(buffer) - 1
                except:
                    print('Invalid tab', end='')
        else:
            buffer.pop(current_tab)
            if current_tab > len(buffer) - 1:
                current_tab = len(buffer) - 1
        # if no tabs are left, quit
        if len(buffer) == 0:
            exit(0)
    elif words[0] == 'goto':
        if len(words) == 3:
            if words[1] == 'tab':
                if words[2] == 'next':
                    current_tab += 1
                    if current_tab > len(buffer) - 1:
                        current_tab = 0
                elif words[2] == 'prev' or words[2] == 'previous':
                    current_tab -= 1
                    if current_tab < 0:
                        current_tab = len(buffer) - 1
                elif int(words[2]) < len(buffer):
                    current_tab = int(words[2]) - 1
                else:
                    print('Invalid tab', end='')
            elif words[1] == 'line':
                try:
                    buffer[current_tab]['cursor'][0] = int(words[2]) - 1
                    # if cursor x > line length, set it to line length
                    if buffer[current_tab]['cursor'][0] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                        buffer[current_tab]['cursor'][0] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
                except:
                    print('Invalid line', end='')
            elif words[1] == 'column':
                try:
                    buffer[current_tab]['cursor'][1] = int(words[2]) - 1
                    # if cursor x > line length, set it to line length
                    if buffer[current_tab]['cursor'][0] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                        buffer[current_tab]['cursor'][0] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
                except:
                    print('Invalid column', end='')
            elif words[1] == 'position':
                pos = words[2].split(':')
                try:
                    buffer[current_tab]['cursor'][0] = int(pos[0]) - 1
                    buffer[current_tab]['cursor'][1] = int(pos[1]) - 1
                    # if cursor x > line length, set it to line length
                    if buffer[current_tab]['cursor'][0] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                        buffer[current_tab]['cursor'][0] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
                except:
                    print('Invalid position', end='')
            else:
                print('Invalid goto', end='')
        else:
            print('Invalid goto', end='')
    elif words[0] == 'save':
        # if no path is given, save to the current path, else save to the given path
        if len(words) > 1:
            buffer[current_tab]['path'] = ' '.join(words[1:])
        if buffer[current_tab]['path'] != None:
            with open(buffer[current_tab]['path'], 'w') as f:
                for line in buffer[current_tab]['content']:
                    f.write(''.join(line) + '\n')

def process_input(key):
    global mode, buffer, current_command
    if mode == 'normal':
        if key.is_sequence:
            if key.name == 'KEY_UP':
                # move cursor up if possible
                if buffer[current_tab]['cursor'][0] > 0:
                    buffer[current_tab]['cursor'][0] -= 1
                # if cursor x > line length, move cursor to end of line
                if buffer[current_tab]['cursor'][1] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                    buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
            elif key.name == 'KEY_DOWN':
                # move cursor down if possible
                if buffer[current_tab]['cursor'][0] < len(buffer[current_tab]['content']) - 1:
                    buffer[current_tab]['cursor'][0] += 1
                # if cursor x > line length, move cursor to end of line
                if buffer[current_tab]['cursor'][1] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]) - 1:
                    buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]) - 1
            elif key.name == 'KEY_LEFT':
                # move cursor left if possible
                if buffer[current_tab]['cursor'][1] > 0:
                    buffer[current_tab]['cursor'][1] -= 1
            elif key.name == 'KEY_RIGHT':
                # move cursor right if possible
                if buffer[current_tab]['cursor'][1] < len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                    buffer[current_tab]['cursor'][1] += 1
            elif key.name == 'KEY_HOME':
                # move cursor to beginning of line
                buffer[current_tab]['cursor'][1] = 0
            elif key.name == 'KEY_END':
                # move cursor to end of line
                buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
            elif key.name == 'KEY_SLEFT' or key.name == 'KEY_SRIGHT':
                # selection mode
                mode = 'selection'
            elif key.name == 'KEY_DELETE' and buffer[current_tab]['cursor'][1] == 0:
                # delete line
                buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]] = []
            elif key.name == 'KEY_ESCAPE':
                # exit
                exit(0)
        else:
            if key == ':':
                mode = 'command'
            elif key == 'i':
                mode = 'insert'
    elif mode == 'command':
        if key.is_sequence:
            if key.name == 'KEY_ESCAPE':
                mode = 'normal'
                current_command = ''
            elif key.name == 'KEY_ENTER':
                mode = 'normal'
                # execute command
                parse_command(current_command)
                current_command = ''
            elif key.name == 'KEY_BACKSPACE':
                # backspace
                if len(current_command) > 0:
                    current_command = current_command[:-1]
        else:
            current_command += key
    elif mode == 'insert':
        # writing to buffer
        if key.is_sequence:
            if key.name == 'KEY_ESCAPE':
                mode = 'normal'
            elif key.name == 'KEY_ENTER':
                buffer[current_tab]['content'].append([]) # add new line
                buffer[current_tab]['cursor'][0] += 1
                buffer[current_tab]['cursor'][1] = 0
            elif key.name == 'KEY_BACKSPACE':
                # backspace
                if buffer[current_tab]['cursor'][1] > 0:
                    # pop character
                    buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]].pop(buffer[current_tab]['cursor'][1] - 1)
                    buffer[current_tab]['cursor'][1] -= 1
                elif buffer[current_tab]['cursor'][0] > 0:
                    # pop line
                    buffer[current_tab]['content'].pop(buffer[current_tab]['cursor'][0])
                    buffer[current_tab]['cursor'][0] -= 1
                    buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
            elif key.name == 'KEY_UP':
                # move cursor up if possible
                if buffer[current_tab]['cursor'][0] > 0:
                    buffer[current_tab]['cursor'][0] -= 1
                # if cursor x > line length, move cursor to end of line
                if buffer[current_tab]['cursor'][1] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                    buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
            elif key.name == 'KEY_DOWN':
                # move cursor down if possible
                if buffer[current_tab]['cursor'][0] < len(buffer[current_tab]['content']) - 1:
                    buffer[current_tab]['cursor'][0] += 1
                # if cursor x > line length, move cursor to end of line
                if buffer[current_tab]['cursor'][1] > len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]) - 1:
                    buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]) - 1
            elif key.name == 'KEY_LEFT':
                # move cursor left if possible
                if buffer[current_tab]['cursor'][1] > 0:
                    buffer[current_tab]['cursor'][1] -= 1
            elif key.name == 'KEY_RIGHT':
                # move cursor right if possible
                if buffer[current_tab]['cursor'][1] < len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]]):
                    buffer[current_tab]['cursor'][1] += 1
            elif key.name == 'KEY_HOME':
                # move cursor to beginning of line
                buffer[current_tab]['cursor'][1] = 0
            elif key.name == 'KEY_END':
                # move cursor to end of line
                buffer[current_tab]['cursor'][1] = len(buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]])
            elif key.name == 'KEY_TAB':
                # insert indentation
                for i in range(4):
                    buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]].insert(buffer[current_tab]['cursor'][1], ' ')
                    buffer[current_tab]['cursor'][1] += 1
        else:
            # add character to buffer
            buffer[current_tab]['content'][buffer[current_tab]['cursor'][0]].insert(buffer[current_tab]['cursor'][1], key)
            buffer[current_tab]['cursor'][1] += 1
    elif mode == 'selection':
        pass

def write_buffer(origin, size, bfr, cursor, scroll):
    # origin: coordinates of the top left corner of the render
    # size: size of the render
    # bfr: nested array of lines and characters
    # cursor: coordinates of the cursor
    # scroll: coordinates of the scroll

    # write the buffer to the terminal
    found_cursor = False
    for ln in range(len(bfr['content'])):
        for ch in range(len(bfr['content'][ln])):
            if origin[1] + ln < size[1] and origin[0] + ch < size[0]:
                with term.location(origin[0] + ch + scroll[0], origin[1] + ln + scroll[1]):
                    if ln == cursor[0] and ch == cursor[1]:
                        found_cursor = True
                        print(term.black_on_white(bfr['content'][ln][ch]), end='')
                    else:
                        print(bfr['content'][ln][ch], end='')
            else:
                print(' ', end='')
    if not found_cursor and cursor[0] + scroll[1] < size[1] and cursor[1] + scroll[0] < size[0]:
        with term.location(cursor[1] + origin[0] + scroll[1], cursor[0] + origin[1] + scroll[0]):
            print(term.black_on_white(' '), end='')
    print()

if __name__ == '__main__':
    with term.fullscreen(), term.hidden_cursor():
        # init script
        config.IDE_init(
            opened_project_path = opened_project_path,
            opened_project_ls = opened_project_ls,
            mode = mode,
            buffer = buffer,
            current_tab = current_tab,
            current_command = current_command,
            parse_command = parse_command,
            write_buffer = write_buffer,
            process_input = process_input
        )
        while True:
            print(term.clear)

            # writing tabs
            tab_size = term.width // len(buffer)
            for i in range(len(buffer)):
                with term.location(i * tab_size, 0):
                    # if selected, print tab in bold white on blue, else print tab in regular colour
                    if i == current_tab:
                        print(config.colour_theme['tab_selected'], end='')
                    else:
                        print(config.colour_theme['tab_unselected'], end='')
                    print(buffer[i]['path'][-tab_size:] if buffer[i]['path'] else 'New File' + ' ' * (tab_size - len(buffer[i]['path'][-tab_size:] if buffer[i]['path'] else 'New File')))
                    print(term.normal, end='')

            # writing line numbers, with dynamic width and colour with scroll offset
            line_number_width = len(str(len(buffer[current_tab]['content'])))
            for i in range(len(buffer[current_tab]['content'])):
                if i < term.height - 2:
                    line_number_colour = config.colour_theme['line_number_other']
                    if buffer[current_tab]['cursor'][0] == i:
                        line_number_colour = config.colour_theme['line_number_current']
                    with term.location(0, i + 1):
                        print(line_number_colour(str(i + 1).rjust(line_number_width)), end='')
            
            # writing buffer with scroll offset
            write_buffer((line_number_width + 1, 1), (term.width, term.height - 2), buffer[current_tab], buffer[current_tab]['cursor'], buffer[current_tab]['scroll'])

            # writing the mode bar
            term_mode_colour = config.colour_theme['normal_mode_bar']
            if mode == 'command':
                term_mode_colour = config.colour_theme['command_mode_bar']
            elif mode == 'insert':
                term_mode_colour = config.colour_theme['insert_mode_bar']
            with term.location(0, term.height - 2):
                print(term_mode_colour(mode.upper() + ' MODE' + ' '*(term.width - len(mode) - len(' MODE'))))
            
            # writing cursor position at the right side of the mode bar
            with term.location(term.width - len(str(buffer[current_tab]['cursor'][0] + 1) + ':' + str(buffer[current_tab]['cursor'][1]+ 1 )), term.height - 2):
                print(term_mode_colour(str(buffer[current_tab]['cursor'][0] + 1) + ':' + str(buffer[current_tab]['cursor'][1] + 1)))

            # writing command bar
            if mode == 'command':
                with term.location(0, term.height - 1):
                    print(':' + current_command, end='')
                with term.location(len(':' + current_command), term.height - 1):
                    print(term.black_on_white(' '), end='') # cursor
                

            # processing input
            try:
                with term.cbreak():
                    k = term.inkey()
                process_input(k)
            except KeyboardInterrupt:
                mode = 'command'
                current_command = 'quit'