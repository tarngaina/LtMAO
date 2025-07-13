from LtMAO import lepath, pyRitoFile


SPACE_CHARS = ' \n\t\r#'
NUM_CHARS = '0123456789.-+e'
ESCAPE_CHARS = {
    '\n': '\\n',
    '\t': '\\t',
    '\r': '\\r',
    "'": "\\'",
    '"': '\\"',
}

def f32_str(num):
    return f'{num:.4f}'.rstrip('0').rstrip('.')

def make_escapes(text):
    for escape_char, made_escape_char in ESCAPE_CHARS.items():
        text = text.replace(escape_char, made_escape_char)
    return text

def clean_escapes(text):
    for escape_char, made_escape_char in ESCAPE_CHARS.items():
        text = text.replace(made_escape_char, escape_char)
    return text

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
    str_type = str_type.replace(' ', '')
    start = -1
    sep = -1
    end = -1
    for i in range(len(str_type)):
        if str_type[i] == '[':
            start = i
        elif str_type[i] == ',':
            sep = i
        elif str_type[i] == ']':
            end = i
    if start == -1:
        return [
            pyRitoFile.bin.BINType[str_type.upper()]
        ]
    if sep == -1:
        return [
            pyRitoFile.bin.BINType[str_type[0:start].upper()], 
            pyRitoFile.bin.BINType[str_type[start+1:end].upper()]
        ]
    else:
        return [
            pyRitoFile.bin.BINType[str_type[0:start].upper()], 
            pyRitoFile.bin.BINType[str_type[start+1:sep].upper()], 
            pyRitoFile.bin.BINType[str_type[sep+1:end].upper()]
        ]

class Reader:
    def __init__(self, text):
        self.text = text
        self.cur = 0
        self.end = len(text)
    
    def human_cur(self):
        index = self.cur - 1
        if not (0 <= index < len(self.text)):
            return None, None
        line = self.text.count('\n', 0, index) + 1
        last_newline_index = self.text.rfind('\n', 0, index)
        column = index - (last_newline_index + 1) if last_newline_index != -1 else index + 1
        return f'Ln: {line}, Col: {column}'

    def read_space(self):
        while self.cur < self.end and self.text[self.cur] in SPACE_CHARS:
            if self.text[self.cur] == '#':
                self.read_until('\n')
            else:
                self.cur += 1

    def read_until(self, end_char):
        start = self.cur
        while self.cur < self.end and self.text[self.cur] != end_char:
            self.cur += 1
        end = self.cur
        self.cur += 1
        return self.text[start:end]
    
    def read_exact(self, expect_char):
        char = self.text[self.cur]
        self.cur += 1
        if char != expect_char:
            raise Exception(f'ritobin: Error: Expect "{expect_char}" but got "{char}" instead at {self.human_cur()}')
    
    def read_non_quote(self):
        start = self.cur
        while self.cur < self.end and self.text[self.cur] not in SPACE_CHARS:
            self.cur += 1
        end = self.cur
        self.cur += 1
        return self.text[start:end]

    def read_quote(self):
        quote = '"'
        self.read_exact(quote)
        start = self.cur
        while self.cur < self.end and self.text[self.cur] != quote or (self.text[self.cur] == quote and self.text[self.cur-1] == '\\'):
            self.cur += 1
        end = self.cur
        self.cur += 1
        return clean_escapes(self.text[start:end])

    def read_hash(self):
        if self.text[self.cur] == '"':
            return self.read_quote()
        else:
            return self.read_non_quote().removeprefix('0x')

    def read_num(self):
        start = self.cur
        while self.cur < self.end and self.text[self.cur] in NUM_CHARS:
            self.cur += 1
        end = self.cur
        self.cur += 1
        return self.text[start:end]
    
    def read_bool(self):
        return False if self.read_non_quote().lower() == 'false' else True
    
    def read_vector(self, vec_size):
        floats = []
        self.read_exact('{')
        for i in range(vec_size):
            self.read_space()
            floats.append(float(self.read_num()))
        self.read_space()
        self.read_exact('}')
        return pyRitoFile.structs.Vector(*floats)
    
    def read_matrix(self):
        floats = []
        self.read_exact('{')
        for i in range(16):
            self.read_space()
            floats.append(float(self.read_num()))
        self.read_space()
        self.read_exact('}')
        return pyRitoFile.structs.Matrix4(*floats)
    
    def read_rgba(self):
        colors = []
        self.read_exact('{')
        for i in range(4):
            self.read_space()
            colors.append(int(self.read_num()))
        self.read_space()
        self.read_exact('}')
        return colors
    
    def read_list_or_list2(self, value_type):
        res = []
        self.read_exact('{')
        while self.cur < self.end:
            self.read_space()
            if self.text[self.cur] == '}':
                self.cur += 1
                break
            else:
                res.append(self.read_value([value_type]))
        return res
    
    def read_pointer_or_embed(self):
        field = pyRitoFile.bin.BINField()
        field.hash_type = self.read_non_quote()
        if field.hash_type == 'null':
            field.hash_type = '00000000'
            field.data = None
        else:
            field.data = []
            self.read_space()
            self.read_exact('{')
            while self.cur < self.end:
                self.read_space()
                if self.text[self.cur] == '}':
                    self.cur += 1
                    break
                else:
                    field.data.append(self.read_field())
        return field

    def read_option(self, value_type):
        self.read_exact('{')
        if self.text[self.cur] == '}':
            self.cur += 1
            return None
        else:
            self.read_space()
            res = self.read_value([value_type])
            self.read_space()
            self.read_exact('}')
        return res
    
    def read_map(self, key_type, value_type):
        res = {}
        self.read_exact('{')
        while self.cur < self.end:
            self.read_space()
            if self.text[self.cur] == '}':
                self.cur += 1
                break
            else:
                key = self.read_value([key_type])
                self.read_space()
                self.read_exact('=')
                self.read_space()
                value = self.read_value([value_type])
                res[key] = value
        return res
    
    read_value_dict = {
        pyRitoFile.bin.BINType.NONE:       lambda: None,
        pyRitoFile.bin.BINType.BOOL:       lambda self, value_types: self.read_bool(),
        pyRitoFile.bin.BINType.I8:         lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.U8:         lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.I16:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.U16:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.I32:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.U32:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.I64:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.U64:        lambda self, value_types: int(self.read_num()),
        pyRitoFile.bin.BINType.F32:        lambda self, value_types: float(self.read_num()),
        pyRitoFile.bin.BINType.VEC2:       lambda self, value_types: self.read_vector(2),
        pyRitoFile.bin.BINType.VEC3:       lambda self, value_types: self.read_vector(3),
        pyRitoFile.bin.BINType.VEC4:       lambda self, value_types: self.read_vector(4),
        pyRitoFile.bin.BINType.MTX44:      lambda self, value_types: self.read_matrix(),
        pyRitoFile.bin.BINType.RGBA:       lambda self, value_types: self.read_rgba(),
        pyRitoFile.bin.BINType.STRING:     lambda self, value_types: self.read_quote(),
        pyRitoFile.bin.BINType.HASH:       lambda self, value_types: self.read_hash(),
        pyRitoFile.bin.BINType.FILE:       lambda self, value_types: self.read_hash(),
        pyRitoFile.bin.BINType.LIST:       lambda self, value_types: self.read_list_or_list2(value_types[1]),
        pyRitoFile.bin.BINType.LIST2:      lambda self, value_types: self.read_list_or_list2(value_types[1]),
        pyRitoFile.bin.BINType.POINTER:    lambda self, value_types: self.read_pointer_or_embed(),
        pyRitoFile.bin.BINType.EMBED:      lambda self, value_types: self.read_pointer_or_embed(),
        pyRitoFile.bin.BINType.OPTION:     lambda self, value_types: self.read_option(value_types[1]),
        pyRitoFile.bin.BINType.MAP:        lambda self, value_types: self.read_map(value_types[1], value_types[2]),
        pyRitoFile.bin.BINType.LINK:       lambda self, value_types: self.read_hash(),
        pyRitoFile.bin.BINType.FLAG:       lambda self, value_types: self.read_bool(),
    }

    def read_value(self, value_types):
        return self.read_value_dict[value_types[0]](self, value_types)
    
    def read_field(self):
        self.read_space()
        field = pyRitoFile.bin.BINField()
        # hash
        field.hash = self.read_hash().rstrip(':')
        self.read_space()
        # type
        str_type = self.read_non_quote()
        field_types = make_types(str_type)
        self.read_space()
        self.read_exact('=')
        self.read_space()
        # data
        field.data = self.read_value(field_types)
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
        
    def read_entry(self):
        self.read_space()
        entry = pyRitoFile.bin.BINEntry()
        # hash
        entry.hash = self.read_hash()
        self.read_space()
        self.read_exact('=')
        self.read_space()
        # type
        entry.type = self.read_hash()
        # rd data
        entry.data = []
        self.read_exact('{')
        while self.cur < self.end:
            self.read_space()
            if self.text[self.cur] == '}':
                self.cur += 1
                break
            else:
                entry.data.append(self.read_field())
        return entry

    def read_header_type(self, bin):
        # pointless because we hardcode writing header in pyRitoFile
        self.read_until('=')
        self.read_space()
        bin.signature = self.read_value(make_types('string'))
        if bin.signature == 'PTCH':
            bin.is_patch = True

    def read_header_version(self, bin):
        # pointless because we hardcode writing header in pyRitoFile
        self.read_until('=')
        self.read_space()
        bin.version = self.read_value(make_types('u32'))

    def read_links(self, bin):
        self.read_until('=')
        self.read_space()
        bin.links = self.read_value(make_types('list[string]'))

    def read_entries(self, bin):
        self.read_until('=')
        self.read_space()

        bin.entries = []
        self.read_exact('{')
        while self.cur < self.end:
            self.read_space()
            if self.text[self.cur] == '}':
                self.cur += 1
                break
            else:
                bin.entries.append(self.read_entry())

    def read_patch(self):
        self.read_space()
        patch = pyRitoFile.bin.BINPatch()
        # hash
        patch.hash = self.read_hash()
        self.read_space()
        self.read_exact('=')
        self.read_space()
        self.read_non_quote()
        self.read_space()
        self.read_exact('{')
        self.read_space()
        # path
        self.read_until('=')
        self.read_space()
        patch.path = self.read_quote()
        self.read_space()
        # type
        self.read_non_quote()
        self.read_space()
        str_type = self.read_non_quote()
        field_types = make_types(str_type)
        patch.type = field_types[0]
        self.read_space()
        self.read_exact('=')
        self.read_space()
        # data
        if field_types[0] in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            field = pyRitoFile.bin.BINField()
            field.type = field_types[0]
            field.value_type = field_types[1]
            field.data = self.read_value(field_types)
            patch.data = field
        else:
            patch.data = self.read_value(field_types)
        self.read_space()
        self.read_exact('}')
        return patch

    def read_patches(self, bin):
        self.read_until('=')
        self.read_space()

        bin.patches = []
        self.read_exact('{')
        while self.cur < self.end:
            self.read_space()
            if self.text[self.cur] == '}':
                self.cur += 1
                break
            else:
                bin.patches.append(self.read_patch())

    def read_blocks(self):
        blocks_to_commands = {
            'type': self.read_header_type,
            'version': self.read_header_version,
            'linked': self.read_links,
            'entries': self.read_entries,
            'patches': self.read_patches,
        }
        max_chars_to_read = max(len(block_header) for block_header in blocks_to_commands)
        res = ''
        while self.cur < self.end and len(res) < max_chars_to_read and res not in blocks_to_commands:
            res += self.text[self.cur]
            self.cur += 1
        if res not in blocks_to_commands:
            raise Exception(f'ritobin: Error: Unexpected block header: {res} at {self.human_cur()}')
        return blocks_to_commands[res]

    def read_text(self):
        bin = pyRitoFile.bin.BIN()
        bin.links = []
        bin.entries = []
        while self.cur < self.end:
            self.read_space()
            self.read_blocks()(bin)
            self.read_space()
        return bin

class Writer:  
    def __init__(self, bin):
        self.bin = bin

    def write_header(self, indent):
        text = f'{add_indent(indent)}#{self.bin.signature}_text\n'
        text += f'{add_indent(indent)}type: string = "{self.bin.signature}"\n'
        text += f'{add_indent(indent)}version: u32 = {self.bin.version}\n'
        return text
    
    def write_links(self, indent):
        text = f'{add_indent(indent)}linked: list[string] = {{'
        if len(self.bin.links) > 0:
            text += '\n'
            for link in self.bin.links:
                text += f'{add_indent(indent+1)}"{link}"\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    def write_value(self, value, value_type, indent, inline=True):
        # complex
        if value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            text = ''
            for v in value.data:
                text += self.write_value(v, value_type, indent, inline=False)
            return text
        elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
            if value.hash_type == '00000000':
                text = f'{add_indent(0 if inline else indent)}null'
            else:
                text = f'{add_indent(0 if inline else indent)}{hash_or_raw(value.hash_type, quote=False)} {{'
                if value.data != None and len(value.data) > 0:
                    text += '\n'
                    for f in value.data:
                        text += self.write_field(f, indent+1)
                    text += f'{add_indent(indent)}}}'
                else:
                    text += '}'
            return text
        # basic
        elif value_type == pyRitoFile.bin.BINType.STRING:
            return f'{add_indent(0 if inline else indent)}"{make_escapes(value)}"'
        elif value_type in (pyRitoFile.bin.BINType.HASH, pyRitoFile.bin.BINType.LINK, pyRitoFile.bin.BINType.FILE):
            return f'{add_indent(0 if inline else indent)}{hash_or_raw(value)}'
        elif value_type == pyRitoFile.bin.BINType.BOOL:
            return f'{add_indent(0 if inline else indent)}{value}'.lower()
        elif value_type == pyRitoFile.bin.BINType.FLAG:
            return f'{add_indent(0 if inline else indent)}{value != 0}'.lower()
        elif value_type == pyRitoFile.bin.BINType.F32:
            return f'{add_indent(0 if inline else indent)}{f32_str(value)}'
        elif value_type in (pyRitoFile.bin.BINType.VEC2, pyRitoFile.bin.BINType.VEC3, pyRitoFile.bin.BINType.VEC4, pyRitoFile.bin.BINType.RGBA):
            values = ', '.join(f'{f32_str(v)}' for v in value)
            return f'{add_indent(0 if inline else indent)}{{ {values} }}'
        elif value_type in (pyRitoFile.bin.BINType.I8, pyRitoFile.bin.BINType.U8,pyRitoFile.bin.BINType.I16,pyRitoFile.bin.BINType.U16,pyRitoFile.bin.BINType.I32,pyRitoFile.bin.BINType.U32,pyRitoFile.bin.BINType.I64,pyRitoFile.bin.BINType.U64):
            return f'{add_indent(0 if inline else indent)}{value}'
        else:
            print(value_type + ' is not sp yet')
    
    def write_list_or_list2(self, field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for value in field.data:
                text += f'{self.write_value(value, field.value_type, indent+1, inline=False)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    def write_pointer_or_embed(self, field, indent):
        if field.hash_type == '00000000':
            text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = null\n'
        else:
            text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = {hash_or_raw(field.hash_type, quote=False)} {{'
            if field.data != None and len(field.data) > 0:
                text += '\n'
                for field in field.data:
                    text += self.write_field(field, indent+1)
                text += f'{add_indent(indent)}}}\n'
            else:
                text += '}\n'
        return text

    def write_option(self, field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if field.data != None:
            text += '\n'
            text += f'{self.write_value(field.data, field.value_type, indent+1, inline=False)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    def write_map(self, field, indent):
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)}[{clean_type(field.key_type)},{clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for key, value in field.data.items():
                text += f'{self.write_value(key, field.key_type, indent+1, inline=False)} = {self.write_value(value, field.value_type, indent+1, inline=True)}\n'
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    def write_matrix(self, field, indent):
        matrix = field.data
        text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = {{\n'
        text += f'{add_indent(indent+1)}{f32_str(matrix.a)}, {f32_str(matrix.b)}, {f32_str(matrix.c)}, {f32_str(matrix.d)}\n'
        text += f'{add_indent(indent+1)}{f32_str(matrix.e)}, {f32_str(matrix.f)}, {f32_str(matrix.g)}, {f32_str(matrix.h)}\n'
        text += f'{add_indent(indent+1)}{f32_str(matrix.i)}, {f32_str(matrix.j)}, {f32_str(matrix.k)}, {f32_str(matrix.l)}\n'
        text += f'{add_indent(indent+1)}{f32_str(matrix.m)}, {f32_str(matrix.n)}, {f32_str(matrix.o)}, {f32_str(matrix.p)}\n'
        text += f'{add_indent(indent)}}}\n'
        return text
    
    def write_field(self, field, indent):
        if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            text = self.write_list_or_list2(field, indent)
        elif field.type in (pyRitoFile.bin.BINType.POINTER, pyRitoFile.bin.BINType.EMBED):
            text = self.write_pointer_or_embed(field, indent)
        elif field.type == pyRitoFile.bin.BINType.OPTION:
            text = self.write_option(field, indent)
        elif field.type == pyRitoFile.bin.BINType.MAP:
            text = self.write_map(field, indent)
        elif field.type == pyRitoFile.bin.BINType.MTX44:
            text = self.write_matrix(field, indent)
        else:
            text = f'{add_indent(indent)}{hash_or_raw(field.hash, quote=False)}: {clean_type(field.type)} = {self.write_value(field.data, field.type, indent)}\n'
        return text
    
    def write_entry(self, entry, indent):
        text = f'{add_indent(indent)}{hash_or_raw(entry.hash)} = {hash_or_raw(entry.type, quote=False)} {{'
        if len(entry.data) > 0:
            text += '\n'
            for field in entry.data:
                text += self.write_field(field, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text

    def write_entries(self, indent):
        text = f'{add_indent(indent)}entries: map[hash,embed] = {{'
        if len(self.bin.entries) > 0:
            text += '\n'
            for entry in self.bin.entries:
                text += self.write_entry(entry, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    def write_patches(self, indent):
        text = f'{add_indent(indent)}patches: map[hash,embed] = {{'
        if len(self.bin.patches) > 0:
            text += '\n'
            for entry in self.bin.patches:
                text += self.write_patch(entry, indent+1)
            text += f'{add_indent(indent)}}}\n'
        else:
            text += '}\n'
        return text
    
    def write_patch(self, patch, indent):
        text = f'{add_indent(indent)}{hash_or_raw(patch.hash)} = patch {{\n'
        text += f'{add_indent(indent+1)}path: string = "{patch.path}"\n'
        text += f'{add_indent(indent+1)}value: '
        if patch.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
            field = patch.data
            text += f'{add_indent(0)}{clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
            if len(field.data) > 0:
                text += '\n'
                for value in field.data:
                    text += f'{self.write_value(value, field.value_type, indent+2, inline=False)}\n'
                text += f'{add_indent(indent+1)}}}\n'
            else:
                text += '}\n'
        elif patch.type in (pyRitoFile.bin.BINType.POINTER, pyRitoFile.bin.BINType.EMBED):
            field = patch.data
            if field.hash_type == '00000000':
                text += f'{add_indent(0)}{clean_type(patch.type)} = null\n'
            else:
                text += f'{add_indent(0)}{clean_type(patch.type)} = {hash_or_raw(field.hash_type, quote=False)} {{'
                if field.data != None and len(field.data) > 0:
                    text += '\n'
                    for f in field.data:
                        text += self.write_field(f, indent+2)
                    text += f'{add_indent(indent+1)}}}\n'
                else:
                    text += '}\n'
        elif patch.type == pyRitoFile.bin.BINType.MTX44:
            matrix = patch.data
            text += f'{add_indent(0)}{clean_type(patch.type)} = {{\n'
            text += f'{add_indent(indent+2)}{f32_str(matrix.a)}, {f32_str(matrix.b)}, {f32_str(matrix.c)}, {f32_str(matrix.d)}\n'
            text += f'{add_indent(indent+2)}{f32_str(matrix.e)}, {f32_str(matrix.f)}, {f32_str(matrix.g)}, {f32_str(matrix.h)}\n'
            text += f'{add_indent(indent+2)}{f32_str(matrix.i)}, {f32_str(matrix.j)}, {f32_str(matrix.k)}, {f32_str(matrix.l)}\n'
            text += f'{add_indent(indent+2)}{f32_str(matrix.m)}, {f32_str(matrix.n)}, {f32_str(matrix.o)}, {f32_str(matrix.p)}\n'
            text += f'{add_indent(indent+1)}}}\n'
        else:
            text += f'{clean_type(patch.type)} = {self.write_value(patch.data, patch.type, indent)}\n'
        text += f'{add_indent(indent)}}}\n'
        return text

    def write_bin(self, indent):
        text = self.write_header(indent)
        text += self.write_links(indent)
        text += self.write_entries(indent)
        if self.bin.is_patch:
            text += self.write_patches(indent)
        return text


def text_to_bin(text_path, bin_path=None):
    if bin_path == None:
        bin_path = '.'.join(text_path.split('.')[:-1] + ['.bin'])
    with pyRitoFile.stream.StringStream.reader(text_path) as ss:
        Reader(ss.read()).read_text().write(bin_path)
    

def bin_to_text(bin_path, text_path=None, hashtables=None):
    if text_path == None:
        text_path = lepath.ext(bin_path, '.bin', '.py')
    bin = pyRitoFile.bin.BIN().read(bin_path)
    if hashtables != None:
        bin.un_hash(hashtables)
    with pyRitoFile.stream.StringStream.writer(text_path) as ss:
        ss.write(Writer(bin).write_bin(0))