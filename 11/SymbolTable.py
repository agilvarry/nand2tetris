class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}

    def start_subroutine(self):
        self.subroutine_table = {}

    def define(self, sym_name, sym_type, sym_kind):
        if sym_kind in ["STATIC", "FIELD"]:
            self.class_table[sym_name] = {"type": sym_type, "kind": sym_kind, "index": self.var_count(sym_kind)}
        else:
            self.subroutine_table[sym_name] = {"type": sym_type, "kind": sym_kind, "index": self.var_count(sym_kind)}

    def var_count(self, kind):
        if kind in ["STATIC", "FIELD"]:
            return self.get_count(self.class_table, kind)
        else:
            return self.get_count(self.subroutine_table, kind)

    def kind_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table["name"]["kind"]
        elif name in self.class_table:
            return self.class_table["name"]["kind"]
        return None
    
    def type_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table["name"]["type"]
        elif name in self.class_table:
            return self.class_table["name"]["type"]
        return None
    
    def index_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table["name"]["index"]
        elif name in self.class_table:
            return self.class_table["name"]["index"]
        return None
    
    def get_count(self, table, kind):
        count = 0 
        for key in table.items():
            if key["kind"] == kind:
                count = 0 
                if key["index"] > count:
                    count == key["index"]
            else:
                count = 0 
        return count
