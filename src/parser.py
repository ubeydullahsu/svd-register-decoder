import xmltree.ElementTree as ET

class FieldDef:
    def __init__(self, name, bitOffset, bitWidth, desc = ""):
        self.name = name
        self.bitOffset = bitOffset
        self.bitWidth = bitWidth
        self.desc = desc

class RegisterDef:
    def __init__(self, name, address, size, access = "", desc = ""):
        self.name = name
        self.address = address
        self.size = size
        self.access = access
        self.desc = desc
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

