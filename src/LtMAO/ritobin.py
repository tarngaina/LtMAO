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
    
def make_types(str_type):
    if '[' in str_type:
        split1 = str_type.split('[')
        split2 = split1[1].split(',')
        res = [split1[0]] + [t.strip(' ').strip(']') for t in split2]
        return [pyRitoFile.bin.BINType[t.upper()] for t in res]
    else:
        return [pyRitoFile.bin.BINType[str_type.upper()]]
    
def beautiful_index(ss):
    index = ss.cur - 1
    if not (0 <= index < len(ss.text)):
        return None, None
    line = ss.text.count('\n', 0, index) + 1
    last_newline_index = ss.text.rfind('\n', 0, index)
    column = index - (last_newline_index + 1) if last_newline_index != -1 else index + 1
    return f'Ln: {line}, Col: {column}'

class Reader:
    @staticmethod
    def init_stream(ss):
        ss.text = ss.read()
        ss.cur = 0
        ss.end = len(ss.text)

    @staticmethod
    def read_space(ss):
        while ss.cur < ss.end and ss.text[ss.cur] in ' \n\t\r': 
            ss.cur += 1

    @staticmethod
    def read_until(ss, end_char):
        start = ss.cur
        while ss.cur < ss.end and ss.text[ss.cur] != end_char:
            ss.cur += 1
        end = ss.cur
        ss.cur += 1
        return ss.text[start:end]
    
    @staticmethod
    def read_exact(ss, expect_char):
        char = ss.text[ss.cur]
        ss.cur += 1
        if char != expect_char:
            raise Exception(f'ritobin: Error: Expect "{expect_char}" but got "{char}" instead at {beautiful_index(ss)}')
    
    @staticmethod
    def read_non_quote(ss):
        start = ss.cur
        while ss.cur < ss.end and ss.text[ss.cur] not in ' \n\t\r':
            ss.cur += 1
        end = ss.cur
        ss.cur += 1
        return ss.text[start:end]

    @staticmethod
    def read_quote(ss):
        quote = '"'
        Reader.read_exact(ss, quote)
        start = ss.cur
        while ss.cur < ss.end and ss.text[ss.cur] != quote:
            ss.cur += 1
        end = ss.cur
        ss.cur += 1
        return ss.text[start:end]

    @staticmethod
    def read_hash(ss):
        if ss.text[ss.cur] == '"':
            return Reader.read_quote(ss).lstrip('0x')
            
        else:
            return Reader.read_non_quote(ss)

    @staticmethod
    def read_num(ss):
        start = ss.cur
        while ss.cur < ss.end and ss.text[ss.cur] in '0123456789.-+e':
            ss.cur += 1
        end = ss.cur
        ss.cur += 1
        return ss.text[start:end]
    
    @staticmethod
    def read_vector(ss, vec_size):
        floats = []
        Reader.read_exact(ss, '{')
        for i in range(vec_size):
            Reader.read_space(ss)
            floats.append(float(Reader.read_num(ss)))
        Reader.read_space(ss)
        Reader.read_exact(ss, '}')
        return pyRitoFile.structs.Vector(*floats)
    
    @staticmethod
    def read_matrix(ss):
        floats = []
        Reader.read_exact(ss, '{')
        for i in range(16):
            Reader.read_space(ss)
            floats.append(float(Reader.read_num(ss)))
        Reader.read_space(ss)
        Reader.read_exact(ss, '}')
        return pyRitoFile.structs.Matrix4(*floats)
    
    @staticmethod
    def read_rgba(ss):
        colors = []
        Reader.read_exact(ss, '{')
        for i in range(4):
            Reader.read_space(ss)
            colors.append(int(Reader.read_num(ss)))
        Reader.read_space(ss)
        Reader.read_exact(ss, '}')
        return colors
    
    @staticmethod
    def read_list_or_list2(ss, value_type):
        res = []
        Reader.read_exact(ss, '{')
        while ss.cur < ss.end:
            Reader.read_space(ss)
            if ss.text[ss.cur] == '}':
                ss.cur += 1
                break
            else:
                res.append(Reader.read_value(ss, [value_type]))
        return res
    
    @staticmethod
    def read_pointer_or_embed(ss):
        field = pyRitoFile.bin.BINField()
        field.hash_type = Reader.read_non_quote(ss)
        if field.hash_type == 'null':
            field.hash_type = '00000000'
            field.data = None
        else:
            field.data = []
            Reader.read_space(ss)
            Reader.read_exact(ss, '{')
            while ss.cur < ss.end:
                Reader.read_space(ss)
                if ss.text[ss.cur] == '}':
                    ss.cur += 1
                    break
                else:
                    field.data.append(Reader.read_field(ss))
        return field
    
    @staticmethod
    def read_option(ss, value_type):
        Reader.read_exact(ss, '{')
        if ss.text[ss.cur] == '}':
            ss.cur += 1
            return None
        else:
            Reader.read_space(ss)
            res = Reader.read_value(ss, [value_type])
            Reader.read_space(ss)
            Reader.read_exact(ss, '}')
        return res
    
    @staticmethod
    def read_map(ss, key_type, value_type):
        res = {}
        Reader.read_exact(ss, '{')
        while ss.cur < ss.end:
            Reader.read_space(ss)
            if ss.text[ss.cur] == '}':
                ss.cur += 1
                break
            else:
                key = Reader.read_value(ss, [key_type])
                Reader.read_space(ss)
                Reader.read_exact(ss, '=')
                Reader.read_space(ss)
                value = Reader.read_value(ss, [value_type])
                res[key] = value
        return res

    @staticmethod
    def read_value(ss, value_types):
        # complex
        # value_types = (list/list2, list_value_type)
        if value_types[0] in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            res = Reader.read_list_or_list2(ss, value_types[1])
        elif value_types[0] in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
            res = Reader.read_pointer_or_embed(ss)
        # value_types = (option, option_value_type)
        elif value_types[0] == pyRitoFile.bin.BINType.OPTION:
            res = Reader.read_option(ss, value_types[1])
        # value_types = (map, map_key_type, map_value_type)
        elif value_types[0] == pyRitoFile.bin.BINType.MAP:
            res = Reader.read_map(ss, value_types[1], value_types[2])
        # basic
        elif value_types[0] in (pyRitoFile.bin.BINType.BOOL, pyRitoFile.bin.BINType.FLAG):
            res = False if Reader.read_non_quote(ss).lower() == 'false' else True
        elif value_types[0] in (pyRitoFile.bin.BINType.U8, pyRitoFile.bin.BINType.U16, pyRitoFile.bin.BINType.U32, pyRitoFile.bin.BINType.U64, pyRitoFile.bin.BINType.I8, pyRitoFile.bin.BINType.I16, pyRitoFile.bin.BINType.I32, pyRitoFile.bin.BINType.I64):
            res = int(Reader.read_num(ss))
        elif value_types[0] == pyRitoFile.bin.BINType.F32:
            res = float(Reader.read_num(ss))
        elif value_types[0] == pyRitoFile.bin.BINType.VEC2:
            res = Reader.read_vector(ss, 2)
        elif value_types[0] == pyRitoFile.bin.BINType.VEC3:
            res = Reader.read_vector(ss, 3)
        elif value_types[0] == pyRitoFile.bin.BINType.VEC4:
            res = Reader.read_vector(ss, 4)
        elif value_types[0] == pyRitoFile.bin.BINType.MTX44:
            res = Reader.read_matrix(ss)
        elif value_types[0] == pyRitoFile.bin.BINType.RGBA:
            res = Reader.read_rgba(ss)
        elif value_types[0] == pyRitoFile.bin.BINType.STRING:
            res = Reader.read_quote(ss)
        elif value_types[0] in (pyRitoFile.bin.BINType.HASH, pyRitoFile.bin.BINType.FILE, pyRitoFile.bin.BINType.LINK):
            res = Reader.read_hash(ss)
        else:
            raise Exception(f'ritobin: Error: {value_types[0]} is not supported at {beautiful_index(ss)}')
        return res
    
    @staticmethod
    def read_field(ss):
        Reader.read_space(ss)
        field = pyRitoFile.bin.BINField()
        # hash
        field.hash = Reader.read_hash(ss).rstrip(':')
        Reader.read_space(ss)
        # type
        str_type = Reader.read_non_quote(ss)
        field_types = make_types(str_type)
        Reader.read_space(ss)
        Reader.read_exact(ss, '=')
        Reader.read_space(ss)
        # data
        field.data = Reader.read_value(ss, field_types)
        # update field
        field.type = field_types[0]
        if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2, pyRitoFile.bin.BINType.OPTION):
            # set value type for list & option
            field.value_type = field_types[1]
        elif field.type in (pyRitoFile.bin.BINType.POINTER, pyRitoFile.bin.BINType.EMBED):
            # set hash type for embed & pointer
            # life hack: read value return a new field 
            # so we set that new field attributes to current field directly
            field.hash_type = field.data.hash_type
            field.data = field.data.data
        elif field.type == pyRitoFile.bin.BINType.MAP:
            # set key, value type for map
            field.key_type = field_types[1]
            field.value_type = field_types[2]
        return field
        
    @staticmethod
    def read_entry(ss):
        Reader.read_space(ss)
        entry = pyRitoFile.bin.BINEntry()
        # hash
        entry.hash = Reader.read_hash(ss)
        Reader.read_space(ss)
        Reader.read_exact(ss, '=')
        Reader.read_space(ss)
        # type
        entry.type = Reader.read_hash(ss)
        # rd data
        entry.data = []
        Reader.read_exact(ss, '{')
        while ss.cur < ss.end:
            Reader.read_space(ss)
            if ss.text[ss.cur] == '}':
                ss.cur += 1
                break
            else:
                entry.data.append(Reader.read_field(ss))
        return entry
    
    @staticmethod
    def read_comment(ss, bin):
        # pointless because its just comment
        comment = Reader.read_until(ss, '\n')

    @staticmethod
    def read_header_type(ss, bin):
        # pointless because we hardcode writing header in pyRitoFile
        Reader.read_until(ss, '=')
        Reader.read_space(ss)
        bin.signature = Reader.read_value(ss, make_types('string'))
        if bin.signature == 'PTCH':
            bin.is_patch = True

    @staticmethod
    def read_header_version(ss, bin):
        # pointless because we hardcode writing header in pyRitoFile
        Reader.read_until(ss, '=')
        Reader.read_space(ss)
        bin.version = Reader.read_value(ss, make_types('u32'))

    @staticmethod
    def read_links(ss, bin):
        Reader.read_until(ss, '=')
        Reader.read_space(ss)
        bin.links = Reader.read_value(ss, make_types('list[string]'))

    @staticmethod
    def read_entries(ss, bin):
        Reader.read_until(ss, '=')
        Reader.read_space(ss)

        bin.entries = []
        Reader.read_exact(ss, '{')
        while ss.cur < ss.end:
            Reader.read_space(ss)
            if ss.text[ss.cur] == '}':
                ss.cur += 1
                break
            else:
                bin.entries.append(Reader.read_entry(ss))

    @staticmethod
    def read_blocks(ss):
        blocks_to_commands = {
            '#': Reader.read_comment,
            'type': Reader.read_header_type,
            'version': Reader.read_header_version,
            'linked': Reader.read_links,
            'entries': Reader.read_entries
        }
        max_chars_to_read = max(len(block_header) for block_header in blocks_to_commands)
        res = ''
        while ss.cur < ss.end and len(res) < max_chars_to_read and res not in blocks_to_commands:
            res += ss.text[ss.cur]
            ss.cur += 1
        if res not in blocks_to_commands:
            raise Exception(f'ritobin: Error: Unexpected block: {res} at {beautiful_index(ss)}')
        return blocks_to_commands[res]

    @staticmethod
    def read_stream(ss):
        Reader.init_stream(ss)

        # init bin object
        bin = pyRitoFile.bin.BIN()
        bin.links = []
        bin.entries = []

        while ss.cur < ss.end:
            Reader.read_space(ss)
            Reader.read_blocks(ss)(ss, bin)
            Reader.read_space(ss)
        return bin
    
    @staticmethod
    def stream_from(text):
        ss = pyRitoFile.stream.StringStream.reader(text.encode('utf-8'), raw=True)
        Reader.init_stream(ss)
        return ss
        


def text_to_bin(text_path, bin_path=None):
    if bin_path == None:
        bin_path = '.'.join(text_path.split('.')[:-1] + ['.bin'])
    with pyRitoFile.stream.StringStream.reader(text_path) as ss:
        Reader.read_stream(ss).write(bin_path)

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
    with pyRitoFile.stream.StringStream.writer(text_path) as ss:
        ss.write(Writer.write_bin(bin, 0))