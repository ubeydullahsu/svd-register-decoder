import xml.etree.ElementTree as ET

class FieldDef:
    def __init__(self, name, bitOffset, bitWidth, desc = ""):
        self.name = name
        self.bitOffset = bitOffset
        self.bitWidth = bitWidth
        self.desc = desc

class RegisterDef:
    def __init__(self, name, address, size, access = "", desc = ""):
        self.name = name
        self.address = address # absolute address (base + offset)
        self.size = size
        self.access = access
        self.desc = desc
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def safe_int_convert(self, value_str):
        try:
            return int(value_str, 0)
        except ValueError:
            return 0

def parse_svd(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    memory_map = []
    
    for peripheral in root.findall(".//peripheral"):
        baseAddress = int(peripheral.find("baseAddress").text, 16) 

        for register in peripheral.findall(".//register"):
            addressOffset = int(register.find("addressOffset").text, 16)
            address = baseAddress + addressOffset
            reg_obj = RegisterDef(
                name=register.find("name").text,
                address=address,
                size=int(register.find("size").text),
                access=register.find("access").text if register.find("access") is not None else "",
                desc=register.find("description").text if register.find("description") is not None else ""
            )

            for field in register.findall(".//field"):
                field_obj = FieldDef(
                    name=field.find("name").text,
                    bitOffset=int(field.find("bitOffset").text),
                    bitWidth=int(field.find("bitWidth").text),
                    desc=field.find("description").text if field.find("description") is not None else ""
                )
                reg_obj.add_field(field_obj)

            memory_map[address] = reg_obj
    
    return memory_map