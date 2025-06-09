from LtMAO import pyRitoFile

def add_indent(indent):
    return indent * 4 * ' '

def clean_type(bin_type):
    return bin_type.name.lower()

def hash_or_raw(name, quote=True):
    if pyRitoFile.bin.BINHasher.is_hash(name):
        return f'0x{name}'
    else:
        return f'"{name}"' if quote else name

def make_type(bin_type_name):
    return pyRitoFile.bin.BINType[bin_type_name.upper()]

class Reader:
    @staticmethod
    def pad_space(text):
        while True:
            char = text.read(1)
            if char != ' ':
                text.seek(text.tell()-1)
                break

    @staticmethod
    def read_include(text, include_text):
        res = ''
        while text.tell() < text.end:
            char = text.read(1)
            if char == '\n': 
                break
            if char != ' ':
                res += char
            if include_text in res:
                break
        return res
    
    @staticmethod
    def read_string(text):
        quote = text.read(1)
        if quote != '"':
            raise Exception(f'ritobin: Error: Expect " but got {quote} instead at {text.tell()}')
        res = ''
        while text.tell() < text.end:
            char = text.read(1)
            if char == quote:
                break
            res += char
        return res

    
    @staticmethod
    def read_numnber(text):
        res = ''
        reach_num = False
        while text.tell() < text.end:
            num = text.read(1) # keep reading until reach num
            if num.isnumeric():
                res += num
                reach_num = True # we reach num
            else: 
                if reach_num: # we reach num but suddenly read char is not num
                    text.seek(text.tell()-1)
                    break #stop because not num anymore
        return res.strip(' ')

    @staticmethod
    def read_type(text):
        return Reader.read_until(text, '=').strip(' ')
    
    @staticmethod
    def read_hash_type(text):
        hash_type = Reader.read_until(text, '{').strip(' ')
        text.seek(text.tell()-1)
        return hash_type

    @staticmethod
    def read_value(text, value_type):
        if '[' in value_type:
            value_types = value_type.split('[')
            first_type = make_type(value_types[0])
            second_type = value_types[1].strip(']')
        else:
            first_type = make_type(value_type)
        res = None
        if first_type == pyRitoFile.bin.BINType.STRING:
            res = Reader.read_string(text)
        elif first_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            res = []
            Reader.read_include(text, '{\n') 
            while True:
                return_offset = text.tell()
                check = Reader.read_include(text, '}')
                if '}' in check:
                    break
                else:
                    text.seek(return_offset)
                    Reader.pad_space(text)
                    value = Reader.read_value(text, second_type)
                    res.append(value)
                    Reader.read_include(text, '\n')
        elif first_type in (pyRitoFile.bin.BINType.U8, pyRitoFile.bin.BINType.U16, pyRitoFile.bin.BINType.U32, pyRitoFile.bin.BINType.U64):
            res = int(Reader.read_numnber(text))
        return res
    

    @staticmethod
    def read_field(text):
        field = pyRitoFile.bin.BINField()
        field.hash = Reader.read_hash(text)
        type = Reader.read_type(text)
        field.type = make_type(type)
        field.data = Reader.read_value(text, type)
        return field
        
    @staticmethod
    def read_entry(text):
        entry = pyRitoFile.bin.BINEntry()
        entry.hash = Reader.read_include(text, '=').replace('=', '').strip(' ')
        Reader.pad_space(text)
        entry.type = Reader.read_include(text, '{\n').replace('{\n', '').strip(' ')
        entry.data = []
        return entry
    
    @staticmethod
    def ignore_comment(text, bin):
        # pointless because its just comment
        comment = Reader.read_include(text, '\n')
        print(f'Comment: {comment}')

    @staticmethod
    def read_header_type(text, bin):
        # pointless because we hardcode writing header in pyRitoFile
        Reader.read_include(text, '=')
        Reader.pad_space(text)
        bin.signature = Reader.read_value(text, 'string')
        if bin.signature == 'PROP':
            bin.is_patch = False
        print(f'Type: {bin.signature}')

    def read_header_version(text, bin):
        # pointless because we hardcode writing header in pyRitoFile
        Reader.read_include(text, '=')
        Reader.pad_space(text)
        bin.version = Reader.read_value(text, 'u32')
        print(f'Version: {bin.version}')

    def read_links(text, bin):
        Reader.read_include(text, '=')
        Reader.pad_space(text)
        bin.links = Reader.read_value(text, 'list[string]')
        print(f'Links: {bin.links}')

    def read_entries(text, bin):
        Reader.read_include(text, '=')
        Reader.pad_space(text)
        Reader.read_include(text, '{\n')
        #while text.tell() < text.end:
        entry = Reader.read_entry(text)
        bin.entries.append(entry)
        print('Finish entries')

    @staticmethod
    def read_and_decide_command(text):
        block_to_commands = {
            '#': Reader.ignore_comment,
            'type': Reader.read_header_type,
            'version': Reader.read_header_version,
            'linked': Reader.read_links,
            'entries': Reader.read_entries
        }
        Reader.pad_space(text)
        res = ''
        while text.tell() < text.end and res not in block_to_commands:
            res += text.read(1)
            if '\n' in res:
                break
        if res not in block_to_commands:
            raise Exception(f'ritobin: Error: Unexpected block: {res} at {text.tell()}')
        return block_to_commands[res]

    @staticmethod
    def read_text(text):
        # init eof pos
        text.seek(0, 2)
        text.end = text.tell()
        text.seek(0)
        # init bin object
        bin = pyRitoFile.bin.BIN()
        bin.links = []
        bin.entries = []

        for i in range(4):
            read_command = Reader.read_and_decide_command(text)
            read_command(text, bin)
            Reader.read_include(text, '\n')
        

        #while text.tell() < text.end:
        #    read_command = Reader.read_and_decide_command(text)
        #    read_command(text, bin)
        #    Reader.read_until(text, '\n')
        return bin


def text_to_bin(text_path, bin_path=None):
    if bin_path == None:
        bin_path = '.'.join(text_path.split('.')[:-1] + ['.bin'])
    with open(text_path, 'r', encoding='utf-8') as text:
        Reader.read_text(text).write(bin_path)

class Writer:   
    @staticmethod 
    def write_header(bin, indent):
        text = f'{add_indent(indent)}#{bin.signature}_text\n'
        text += f'{add_indent(indent)}type: string = "{bin.signature}"\n'
        text += f'{add_indent(indent)}version: u32 = {bin.version}\n'
        return text
    
    @staticmethod
    def write_links(links, indent):
        text = f'{add_indent(indent)}linked: list[string] = {{'
        if len(links) > 0:
            text += '\n'
            for link in links:
                text += f'{add_indent(indent+1)}"{link}"\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    @staticmethod
    def write_value(value, value_type, indent):
        # complex
        if value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            text = ''
            for v in value.data:
                text += Writer.write_value(v, value_type, indent)
            return text
        elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
            text = f'{add_indent(indent)}{hash_or_raw(value.hash_type, quote=False)} {{'
            if value.data != None and len(value.data) > 0:
                text += '\n'
                for f in value.data:
                    text += Writer.write_field(f, indent+1)
                text += f'{add_indent(indent)}}}'
            else:
                text += '}'
            return text
        # basic
        elif value_type == pyRitoFile.bin.BINType.STRING:
            return f'{add_indent(indent)}"{value}"'
        elif value_type in (pyRitoFile.bin.BINType.HASH, pyRitoFile.bin.BINType.LINK):
            return f'{add_indent(indent)}{hash_or_raw(value)}'
        elif value_type == pyRitoFile.bin.BINType.BOOL:
            return f'{add_indent(indent)}{value}'.lower()
        elif value_type == pyRitoFile.bin.BINType.FLAG:
            return f'{add_indent(indent)}{value != 0}'.lower()
        elif value_type == pyRitoFile.bin.BINType.F32:
            return f'{add_indent(indent)}{value:g}'
        elif value_type in (pyRitoFile.bin.BINType.VEC2, pyRitoFile.bin.BINType.VEC3, pyRitoFile.bin.BINType.VEC4, pyRitoFile.bin.BINType.RGBA):
            values = ", ".join(f'{v:.9g}' for v in value)
            return f'{add_indent(indent)}{{ {values} }}'
        return f'{add_indent(indent)}{value}'
    
    @staticmethod
    def write_list_or_list2(field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for value in field.data:
                text += f'{Writer.write_value(value, field.value_type, indent+1)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    @staticmethod
    def write_pointer_or_embed(field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = {hash_or_raw(field.hash_type, quote=False)} {{'
        if field.data != None and len(field.data) > 0:
            text += '\n'
            for field in field.data:
                text += Writer.write_field(field, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    @staticmethod
    def write_option(field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if field.data != None:
            text += '\n'
            text += f'{Writer.write_value(field.data, field.value_type, indent+1)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    @staticmethod
    def write_map(field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.key_type)},{clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for key, value in field.data.items():
                text += f'{Writer.write_value(key, field.key_type, indent+1)} = {Writer.write_value(value, field.value_type, 0)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    @staticmethod
    def write_field(field, indent):
        if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            text = Writer.write_list_or_list2(field, indent)
        elif field.type in (pyRitoFile.bin.BINType.POINTER, pyRitoFile.bin.BINType.EMBED):
            text = Writer.write_pointer_or_embed(field, indent)
        elif field.type == pyRitoFile.bin.BINType.OPTION:
            text = Writer.write_option(field, indent)
        elif field.type == pyRitoFile.bin.BINType.MAP:
            text = Writer.write_map(field, indent)
        else:
            text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = {Writer.write_value(field.data, field.type, 0)}\n'
        return text
    
    @staticmethod
    def write_entry(entry, indent):
        text = f'{add_indent(indent)}{hash_or_raw(entry.hash)} = {hash_or_raw(entry.type, quote=False)} {{'
        if len(entry.data) > 0:
            text += '\n'
            for field in entry.data:
                text += Writer.write_field(field, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    @staticmethod
    def write_entries(entries, indent):
        text = f'{add_indent(indent)}entries: map[hash,embed] = {{'
        if len(entries) > 0:
            text += '\n'
            for entry in entries:
                text += Writer.write_entry(entry, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    @staticmethod
    def write_bin(bin, indent):
        text = Writer.write_header(bin, indent)
        text += Writer.write_links(bin.links, indent)
        text += Writer.write_entries(bin.entries, indent)
        return text


def bin_to_text(bin_path, text_path=None, hashtables=None):
    if text_path == None:
        text_path = bin_path.replace('.bin', '.py')
    bin = pyRitoFile.bin.BIN().read(bin_path)
    if hashtables != None:
        bin.un_hash(hashtables)
    with open(text_path, 'w+', encoding='utf-8') as f:
        f.write(Writer.write_bin(bin, 0))