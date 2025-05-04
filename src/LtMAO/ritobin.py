from LtMAO import pyRitoFile

def add_indent(indent):
    return indent * 4 * ' '

def clean_type(bin_type):
    return bin_type.name.lower()

class Reader:
    pass

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
        return text
    
    @staticmethod
    def write_value(value, value_type, indent):
        # complex
        if value_type in (pyRitoFile.BINType.LIST, pyRitoFile.BINType.LIST2):
            text = ''
            for v in value.data:
                text += Writer.write_value(v, value_type, indent)
            return text
        elif value_type in (pyRitoFile.BINType.EMBED, pyRitoFile.BINType.POINTER):
            text = f'{add_indent(indent)}{value.hash_type} = {{'
            if len(value.data) > 0:
                text += '\n'
                for f in value.data:
                    text += Writer.write_field(f, indent+1)
            text += f'{add_indent(indent)}}}'
            return text
        # basic
        elif value_type in (pyRitoFile.BINType.STRING, pyRitoFile.BINType.HASH, pyRitoFile.BINType.LINK):
            return f'{add_indent(indent)}"{value}"'
        elif value_type in (pyRitoFile.BINType.VEC2, pyRitoFile.BINType.VEC3, pyRitoFile.BINType.VEC4, pyRitoFile.BINType.RGBA):
            return f'{add_indent(indent)}{{ {", ".join(str(v) for v in value)} }}'
        return f'{add_indent(indent)}{value}'
    
    @staticmethod
    def write_list_or_list2(field, indent):
        text = f'{add_indent(indent)}{field.hash}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for value in field.data:
                text += f'{Writer.write_value(value, field.value_type, indent+1)}\n'
        text += f'{add_indent(indent)}}}\n'
        return text
    
    @staticmethod
    def write_pointer_or_embed(field, indent):
        text = f'{add_indent(indent)}{field.hash}: {clean_type(field.type)} = {field.hash_type} {{'
        if len(field.data) > 0:
            text += '\n'
            for field in field.data:
                text += Writer.write_field(field, indent+1)
        text += f'{add_indent(indent)}}}\n'
        return text

    @staticmethod
    def write_option(field, indent):
        text = f'{add_indent(indent)}{field.hash}: {clean_type(field.type)}[{clean_type(field.value_type)}] = {{'
        if field.data != None:
            text += '\n'
            text += f'{Writer.write_value(field.data, field.value_type, indent+1)}\n'
        text += f'{add_indent(indent)}}}\n'
        return text

    @staticmethod
    def write_map(field, indent):
        text = f'{add_indent(indent)}{field.hash}: {clean_type(field.type)}[{clean_type(field.key_type)}, {clean_type(field.value_type)}] = {{'
        if len(field.data) > 0:
            text += '\n'
            for key, value in field.data.items():
                text += f'{Writer.write_value(key, field.key_type, indent+1)} = {Writer.write_value(value, field.value_type, 0)}\n'
        text += f'{add_indent(indent)}}}\n'
        return text

    @staticmethod
    def write_field(field, indent):
        if field.type in (pyRitoFile.BINType.LIST, pyRitoFile.BINType.LIST2):
            text = Writer.write_list_or_list2(field, indent)
        elif field.type in (pyRitoFile.BINType.POINTER, pyRitoFile.BINType.EMBED):
            text = Writer.write_pointer_or_embed(field, indent)
        elif field.type == pyRitoFile.BINType.OPTION:
            text = Writer.write_option(field, indent)
        elif field.type == pyRitoFile.BINType.MAP:
            text = Writer.write_map(field, indent)
        else:
            text = f'{add_indent(indent)}{field.hash}: {clean_type(field.type)} = {Writer.write_value(field.data, field.type, 0)}\n'
        return text
    
    @staticmethod
    def write_entry(entry, indent):
        text = f'{add_indent(indent)}"{entry.hash}" = {entry.type} {{'
        if len(entry.data) > 0:
            text += '\n'
            for field in entry.data:
                text += Writer.write_field(field, indent+1)
        text += f'{add_indent(indent)}}}\n'
        return text

    @staticmethod
    def write_entries(entries, indent):
        text = f'{add_indent(indent)}entries: map[hash,embed] = {{'
        if len(entries) > 0:
            text += '\n'
            for entry in entries:
                text += Writer.write_entry(entry, indent+1)
        text += f'{add_indent(indent)}}}\n'
        return text

    @staticmethod
    def write_bin(bin: pyRitoFile.BIN, indent):
        text = Writer.write_header(bin, indent)
        text += Writer.write_links(bin.links, indent)
        text += Writer.write_entries(bin.entries, indent)
        return text


def bin_to_text(bin_path, text_path=None, hashtables=None):
    if text_path == None:
        text_path = bin_path.replace('.bin', '.py')
    bin = pyRitoFile.read_bin(bin_path)
    if hashtables != None:
        bin.un_hash(hashtables)
    with open(text_path, 'w+') as f:
        f.write(Writer.write_bin(bin, 0))