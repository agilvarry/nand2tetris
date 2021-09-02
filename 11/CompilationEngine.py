import xml.etree.ElementTree as ET
from SymbolTable import SymbolTable
import VMWriter


def write_vm(file_name, out_vm):
    out_folder = r'C:\Users\agilvarry\Documents\github\nand2tetris\11\ConvertToBin\output'
    compilation_out=open(f"{out_folder}\\{file_name}.vm", "w")
    compilation_out.write(out_vm)


math_functions = {
    "multiply": 2,
    "divide": 2,
    "min": 2,
    "max": 2,
    "sqrt": 1
}
string_functions = {
    "new": 1,
    "dispose": 0,
    "length": 0,
    "chatAt": 1,
    "setCharAt": 1,
    "appendChar": 1,
    "eraseLastChar": 0,
    "intValue": 0,
    "setInt": 1,
    "backSpace": 0,
    "doubleQuote": 0,
    "newLine": 0
}
array_functions = {
    "new": 1,
    "dispose": 0
}
output_functions = {
    "moveCursor": 2,
    "printChar": 1,
    "printString": 1,
    "printInt": 1,
    "printLn": 0,
    "backSpace": 0
}
screen_functions = {
    "clearScreen":0,
    "setColor":1,
    "drawPixel":2,
    "drawLine":4,
    "drawRectangle":4,
    "drawCircle":3
}
keyboard_functions = {
    "keyPressed":0,
    "readChar": 0,
    "readLine":1,
    "readInt":1
}
memory_functions = {
    "peek":1,
    "poke":2,
    "alloc":1,
    "deAlloc":1
}
sys_functions = {
    "halt":0,
    "error":0,
    "wait":1
}
os_classes = {
    "Math":  math_functions,
    "String": string_functions,
    "Array": array_functions,
    "Output": output_functions,
    "Screen": screen_functions,
    "Keyboard": keyboard_functions,
    "Memory": memory_functions,
    "Sys": sys_functions
}
math_ops = {
    "+": "add",
    "-": "sub",
    "/": "div",
    ">": "gt",
    "<": "lt",
    "=": "eq",
    "&": "and"
}


class CompilationEngine:
    def __init__(self, xml_in):
        self.in_statements = False
        self.nested_expression = False
        self.xml_in = xml_in
        self.tables = SymbolTable()
        self.class_name = ""
        self.label_end = 0
        self.args = 0

    def compile_class(self, out_vm, tokens):
        """
        set class name variable,drop unneeded tokens
        """
        tokens.pop(0)  # remove class keyword
        self.class_name = tokens[0][1].strip()
        tokens.pop(0)  # remove class name identifier
        tokens.pop(0)  # remove opening bracket

        # go into loop through rest of class
        while tokens[0][1].strip() != '}':
            out_vm, tokens = self.token_handler(out_vm, tokens)

        tokens.pop(0)  # remove closing braket

        return out_vm, tokens

    def token_handler(self, out_vm, tokens):
        current = tokens[0]
        tag, token = current[0], current[1].strip()
        print(tokens[0])
        if token in self.non_terminal:
            if token == 'class':
                out_vm, tokens = self.compile_class(out_vm, tokens)
            elif token in ['static', 'field']:
                out_vm, tokens = self.compile_class_var_dec(out_vm, tokens)
            elif token in ['constructor', 'function', 'method']:
                out_vm, tokens = self.compile_subroutine_dec(out_vm, tokens)
            elif token == 'var':
                out_vm, tokens = self.compile_var_dec(out_vm, tokens)
            elif token in ['let', 'if', 'while', 'do', 'return']:
                out_vm, tokens = self.compile_statements(out_vm, tokens)

        return out_vm, tokens

    def compile_class_var_dec(self, out_vm, tokens):
        """
        set first classVarDec and keyword tags,drop first time
        iterate through remaining tags until we find semicolon
        then wrap things up
        """

        sym_kind = tokens[0][1].strip()
        tokens.pop(0)
        sym_type = tokens[1][1].strip()
        tokens.pop(0)

        while tokens[0][1].strip() != ';':
            if tokens[0][1].strip() != ',':
                # maybe add 'field' count here? id sym_kind == field?  # TODO
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            tokens.pop(0)

        tokens.pop(0) # drop ';'

        return out_vm, tokens

    def compile_subroutine_dec(self, out_vm, tokens):
        """
        initiate subroutine symbol table
        """
        self.tables.start_subroutine()
        # maybe counting if, while, var here? #TODO

        if tokens[0][1].strip() == 'method':
            self.tables.define('this', self.class_name, 'argument')

        tokens.pop(0)  # pop funtion, method, constructor keyword.
        ret_type = tokens[0][1].strip()  # void, int, etc
        tokens.pop(0)  # drop ret type
        sub_name = f"{self.class_name}.{tokens[0][1].strip()}"
        tokens.pop(0)  # drop sub name

        tokens = self.compile_parameter_list(tokens)
        out_vm, tokens = self.compile_subroutine_body(out_vm, tokens, sub_name)

        # param_count = self.tables.var_count('argument') #get list of parameters

        # out_fun = VMWriter.write_function(sub_name, param_count) #nLocals might be more than this
        # out_vm = out_fun+out_vm #idkidkidkidk
        return out_vm, tokens

    def compile_parameter_list(self, tokens):
        """
        iterate through remaining tags until we find closing paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        tokens.pop(0)  # drop open paren

        # sets the sumbol type and kind, if there are any symbols
        sym_type = tokens[0][1].strip()  # int, Object, etc.
        sym_kind = 'argument'

        # loop through symbols till we hit a closing paren

        while tokens[0][1].strip() != ')':
            if tokens[0][0] == 'identifier':
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            elif tokens[0][1].strip() == ',':  # new parameter coming, look ahead for type
                sym_type = tokens[1][1].strip()  # int, Object, etc.
            tokens.pop(0)  # drop token

        tokens.pop(0)  # drop closing paren
        return tokens

    def compile_subroutine_body(self, out_vm, tokens, sub_name):
        """
        set first parameterList and call token handler for open bracket
        iterate through remaining tags until we find closing bracket
        then wrap up
        """
        tokens.pop(0)  # pop open bracket

        while tokens[0][1].strip() != '}':
            if tokens[0][1].strip() == "var":
                tokens = self.compile_var_dec(tokens)
            else:
                param_count = self.tables.var_count('local')  # get list of parameters
                out_vm = out_vm + VMWriter.write_function(sub_name, param_count)  # get list of parameters
                out_vm, tokens = self.compile_statements(out_vm, tokens)
        tokens.pop(0)  # pop close bracket

        return out_vm, tokens

    def compile_var_dec(self, tokens):
        sym_kind = 'local'
        tokens.pop(0)
        sym_type = tokens[1][1].strip() #boolean, int, etc.
        tokens.pop(0)

        while tokens[0][1].strip() != ';':
            if tokens[0][0] == 'identifier' and tokens[1][0] != 'identifier': #TODO this handles if an Object is the var type. Maybe not good enough?
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            tokens.pop(0)  # drop sym_type, var
        tokens.pop(0)  # drop ;

        return tokens

    def compile_statements(self, out_vm, tokens):
        """
        check if we're in a statements block or not to initialize or not 
        """
        if not self.in_statements:
            self.in_statements = True

        statements_list = ['let', 'if', 'while', 'do', 'return']

        while tokens[0][1].strip() in statements_list:
            token = tokens[0][1].strip()
            if token == 'let':
                out_vm, tokens = self.compile_let(out_vm, tokens)
            elif token == 'if':
                out_vm, tokens = self.compile_if(out_vm, tokens)
            elif token == 'return':
                out_vm, tokens = self.compile_return(out_vm, tokens)
            elif token == 'do':
                out_vm, tokens = self.compile_do(out_vm, tokens)
            elif token == 'while':
                out_vm, tokens = self.compile_while(out_vm, tokens)

        self.in_statements = False

        return out_vm, tokens

    def compile_let(self, out_vm, tokens):

        tokens.pop(0) #drop let
        var_name = tokens[0][1].strip()
        tokens.pop(0)  # drop varName
        sym_kind = self.tables.kind_of(var_name)
        sym_idx = self.tables.index_of(var_name)

        if tokens[1][1].strip() == '[': #TODO some arr stuff
            tokens.pop(0) # [
            out_vm, tokens = self.compile_expression(out_vm, tokens)
            tokens.pop(0)  # ]            

        tokens.pop(0)  # drop =
        out_vm, tokens = self.compile_expression(out_vm, tokens)  # expression
        tokens.pop(0)  # drop ;
        out_vm = out_vm + VMWriter.write_pop(sym_kind, sym_idx)
        return out_vm, tokens

    def compile_do(self, out_vm, tokens):
        """
        get Method call info, call expression list
        """
        tokens.pop(0)  # drop do
        while tokens[0][1].strip() != ';':
            if tokens[0][1].strip() == '(':
                tokens.pop(0)  # drop ()
                out_vm, tokens = self.compile_expression_list(out_vm, tokens)
            elif tokens[0][1].strip() == ')':
                tokens.pop(0)  # drop ()
            else:
                out_vm, tokens= self.compile_expression_list(out_vm, tokens)
        # out_vm, tokens = self.compile_subroutine_call(out_vm, tokens)

        tokens.pop(0)  # drop ;
        out_vm = out_vm + "pop temp 0\n"

        return out_vm, tokens

    def compile_while(self, out_vm, tokens):
        self.label_end = self.label_end + 1
        out_vm = out_vm + VMWriter.write_label(f"WHILE_EXP{self.label_end}")
        tokens.pop(0)  # drop while
        tokens.pop(0)  # drop (
        out_vm, tokens = self.compile_expression(out_vm, tokens)
        tokens.pop(0)  # drop )
        out_vm = out_vm + VMWriter.write_arithmetic("not")
        out_vm = out_vm + VMWriter.write_if(f"WHILE_EXP{self.label_end}")
        tokens.pop(0)  # drop {
        self.in_statements = False  # risky flag flipping
        out_vm, tokens = self.compile_statements(out_vm, tokens)  # statement
        self.in_statements = True  # risky flag flipping
        tokens.pop(0)  # drop }

        out_vm = out_vm + VMWriter.write_goto(f"WHILE_EXP{self.label_end}")
        out_vm = out_vm + VMWriter.write_label(f"WHILE_END{self.label_end}")

        return out_vm, tokens

    def compile_return(self, out_vm, tokens):
        tokens.pop(0)  # drop return

        while tokens[0][1].strip() != ';':
            out_vm, tokens = self.compile_expression(out_vm, tokens)

        tokens.pop(0)  # ;
        out_vm = out_vm + VMWriter.write_return()  # TODO void?
        return out_vm, tokens

    def compile_if(self, out_vm, tokens):
        self.label_end = self.label_end + 1
        tokens.pop(0)  # drop while
        tokens.pop(0)  # drop (
        out_vm, tokens = self.compile_expression(out_vm, tokens)
        tokens.pop(0)  # drop )
        out_vm = out_vm + VMWriter.write_if(f"IF_TRUE{self.label_end}")
        out_vm = out_vm + VMWriter.write_goto(f"IF_FALSE{self.label_end}")
        out_vm = out_vm + VMWriter.write_label(f"IF_TRUE{self.label_end}")
        tokens.pop(0)  # drop {
        self.in_statements = False  # risky flag flipping
        out_vm, tokens = self.compile_statements(out_vm, tokens)  # statement
        self.in_statements = True  # risky flag flipping
        tokens.pop(0)  # drop }
        out_vm = out_vm + VMWriter.write_goto(f"END{self.label_end}")
        out_vm = out_vm + VMWriter.write_label(f"IF_FALSE{self.label_end}")
        if tokens[0][1].strip() == "else":
            tokens.pop(0)  # drop else
            tokens.pop(0)  # drop braket
            self.in_statements = False  # risky flag flipping
            out_vm, tokens = self.compile_statements(out_vm, tokens)  # statement
            self.in_statements = True  # risky flag flipping
            tokens.pop(0)  # drop braket
        out_vm = out_vm + VMWriter.write_label(f"END{self.label_end}")
        return out_vm, tokens

    def compile_expression(self, out_vm, tokens):
        if tokens[0][1].strip() == '(':
            tokens.pop(0)  # drop (
            out_vm, tokens = self.compile_expression(out_vm, tokens)
            tokens.pop(0)  # drop )
        else:
            out_vm, tokens = self.compile_term(out_vm, tokens)

        while tokens[0][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            token = tokens[0][1].strip()
            tokens.pop(0)  # drop token
            out_vm, tokens = self.compile_term(out_vm, tokens)
            if token == '/':
                out_vm = out_vm + VMWriter.write_call('Math.divide', 2)
            elif token == '*':
                out_vm = out_vm + VMWriter.write_call('Math.multiply', 2)
            else:
                out_vm = out_vm + VMWriter.write_arithmetic(math_ops[token])
        return out_vm, tokens

    def compile_expression_list(self, out_vm, tokens):
        self.args = 0
        while tokens[0][1].strip() not in [';',')']:
            if tokens[0][1].strip() == ',':
                tokens.pop(0)  # drop ,
            else:
                self.args = self.args + 1
                out_vm, tokens = self.compile_expression(out_vm, tokens)

        return out_vm, tokens

    def compile_term(self, out_vm, tokens):
        token = tokens[0][1].strip()
        tag = tokens[0][0].strip()
        if tag == 'symbol':
            if token == '(':
                self.nested_expression = True
                tokens.pop(0)  # drop (
                out_vm, tokens = self.compile_expression(out_vm, tokens)
                tokens.pop(0)  # drop )
                self.nested_expression = False
            elif token in ['-', '~']:
                tokens.pop(0)  # drop symbol
                out_vm, tokens = self.compile_term(out_vm, tokens)
                if token == '-':
                    out_vm = out_vm + VMWriter.write_arithmetic('neg')
                else:
                    out_vm = out_vm + VMWriter.write_arithmetic('not')
        elif tag == 'integerConstant':
            out_vm = out_vm + VMWriter.write_push("constant", token)
            tokens.pop(0)
        elif tag == 'stringConstant':
            out_vm = out_vm + VMWriter.write_push('constant', len(token))  # more work to understand here
            out_vm = out_vm + VMWriter.write_call('String.new', 1)
            for c in token:
                out_vm = out_vm + VMWriter.write_push('constant', ord(c))
                out_vm = out_vm + VMWriter.write_call('String.appendChar', 2)
            tokens.pop(0)

        elif tag == 'keyword':
            if token == "true":
                out_vm = out_vm + VMWriter.write_push("constant", 0)
                out_vm = out_vm + VMWriter.write_arithmetic("not")
            if token in ["false", 'null']:
                out_vm = out_vm + VMWriter.write_push("constant", 0)
            elif token == 'this':
                out_vm = out_vm + VMWriter.write_push("pointer", 0)
            tokens.pop(0)

        elif tokens[0][0] == 'identifier':
            nargs=0
            name = token
            kind = self.tables.kind_of(token)
            idx = self.tables.index_of(token)

            id = tokens[0][1].strip()  # identifier
            tokens.pop(0)
            print(name)

            if tokens[0][1].strip() in ['[', '(']:
                tokens.pop(0)  # [,()
                out_vm, tokens = self.compile_expression(out_vm, tokens)
                tokens.pop(0)  # ],)
            elif tokens[0][1].strip() == '.':
                tokens.pop(0)  # drop '.'
                id = f"{id}.{tokens[0][1].strip()}"
                tokens.pop(0)  # drop identifier
                tokens.pop(0)  # drop '('
                out_vm, tokens= self.compile_expression_list(out_vm, tokens)

                out_vm = out_vm + VMWriter.write_call(id, self.args)
                tokens.pop(0)  # drop')'
            elif tokens[0][1].strip() == '(':
                tokens.pop(0)  # (
                out_vm, tokens= self.compile_expression_list(out_vm, tokens)
                tokens.pop(0)  # )

        return out_vm, tokens

    non_terminal = [
        'class',
        'static',
        'field',
        'constructor',
        'function',
        'method',
        'var',
        'let',
        'if',
        'while',
        'return',
        'do'
    ]

    def Engine(self):
        root = ET.fromstring(self.xml_in)
        out_vm = ""

        # create list of tags and tokens
        tokens = []
        for child in root:
            tokens.append([child.tag,child.text])

        while len(tokens) > 1:
            out_vm, tokens = self.token_handler(out_vm, tokens)

        return out_vm