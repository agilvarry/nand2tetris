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
        self.vm_out = ""
        self.tokens = []
        self.tables = SymbolTable()
        self.class_name = ""
        self.label_end = 0
        self.args = 0

    def next_token(self):
        self.tokens.pop(0)
        print(self.tokens)

    def write_vm(self,vm):
        self.vm_out = self.vm_out + vm  

    def compile_class(self):
        """
        set class name variable,drop unneeded tokens
        """
        self.next_token()  # remove class keyword
        self.class_name = self.tokens[0][1].strip()
        self.next_token()  # remove class name identifier
        self.next_token()  # remove opening bracket

        # go into loop through rest of class
        while self.tokens[0][1].strip() != '}':
            self.token_handler()

        self.next_token()  # remove closing braket

    def token_handler(self):
        current = self.tokens[0]
        token = current[1].strip()

        if token in self.non_terminal:
            if token == 'class':
                self.compile_class()
            elif token in ['static', 'field']:
                self.compile_class_var_dec()
            elif token in ['constructor', 'function', 'method']:
                self.compile_subroutine_dec()
            elif token == 'var':
                self.compile_var_dec()
            elif token in ['let', 'if', 'while', 'do', 'return']:
                self.compile_statements()

    def compile_class_var_dec(self):
        """
        set first classVarDec and keyword tags,drop first time
        iterate through remaining tags until we find semicolon
        then wrap things up
        """

        sym_kind = self.tokens[0][1].strip()
        self.next_token()
        sym_type = self.tokens[1][1].strip()
        self.next_token()

        while self.tokens[0][1].strip() != ';':
            if self.tokens[0][1].strip() != ',':
                # maybe add 'field' count here? id sym_kind == field?  # TODO
                self.tables.define(self.tokens[0][1].strip(), sym_type, sym_kind)
            self.next_token()

        self.next_token() # drop ';'


    def compile_subroutine_dec(self):
        """
        initiate subroutine symbol table
        """
        self.tables.start_subroutine()
        # maybe counting if, while, var here? #TODO

        if self.tokens[0][1].strip() == 'method':
            self.tables.define('this', self.class_name, 'argument')

        self.next_token()  # pop funtion, method, constructor keyword.
        ret_type = self.tokens[0][1].strip()  # void, int, etc
        self.next_token()  # drop ret type
        sub_name = f"{self.class_name}.{self.tokens[0][1].strip()}"
        self.next_token()  # drop sub name

        self.compile_parameter_list()
        self.compile_subroutine_body(sub_name)

        # param_count = self.tables.var_count('argument') #get list of parameters

        # out_fun = VMWriter.write_function(sub_name, param_count) #nLocals might be more than this
        # out_vm = out_fun+out_vm #idkidkidkidk

    def compile_parameter_list(self):
        """
        iterate through remaining tags until we find closing paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        self.next_token()  # drop open paren

        # sets the sumbol type and kind, if there are any symbols
        sym_type = self.tokens[0][1].strip()  # int, Object, etc.
        sym_kind = 'argument'

        # loop through symbols till we hit a closing paren

        while self.tokens[0][1].strip() != ')':
            if self.tokens[0][0] == 'identifier':
                self.tables.define(self.tokens[0][1].strip(), sym_type, sym_kind)
            elif self.tokens[0][1].strip() == ',':  # new parameter coming, look ahead for type
                sym_type = self.tokens[1][1].strip()  # int, Object, etc.
            self.next_token()  # drop token

        self.next_token()  # drop closing paren

    def compile_subroutine_body(self, sub_name):
        """
        set first parameterList and call token handler for open bracket
        iterate through remaining tags until we find closing bracket
        then wrap up
        """
        self.next_token()  # pop open bracket

        while self.tokens[0][1].strip() != '}':
            if self.tokens[0][1].strip() == "var":
                self.compile_var_dec()
            else:
                param_count = self.tables.var_count('local')  # get list of parameters
                out_vm = VMWriter.write_function(sub_name, param_count)  # get list of parameters
                self.write_vm(out_vm) 
                self.compile_statements()
        self.next_token()  # pop close bracket

    def compile_var_dec(self):
        sym_kind = 'local'
        self.next_token()
        sym_type = self.tokens[1][1].strip() #boolean, int, etc.
        self.next_token()

        while self.tokens[0][1].strip() != ';':
            if self.tokens[0][0] == 'identifier' and self.tokens[1][0] != 'identifier': #TODO this handles if an Object is the var type. Maybe not good enough?
                self.tables.define(self.tokens[0][1].strip(), sym_type, sym_kind)
            self.next_token()  # drop sym_type, var
        self.next_token()  # drop ;

    def compile_statements(self):
        """
        check if we're in a statements block or not to initialize or not 
        """
        if not self.in_statements:
            self.in_statements = True

        statements_list = ['let', 'if', 'while', 'do', 'return']

        while self.tokens[0][1].strip() in statements_list:
            token = self.tokens[0][1].strip()
            if token == 'let':
                self.compile_let()
            elif token == 'if':
                self.compile_if()
            elif token == 'return':
                self.compile_return()
            elif token == 'do':
                self.compile_do()
            elif token == 'while':
                self.compile_while()

        self.in_statements = False

    def compile_let(self):

        self.next_token() #drop let
        var_name = self.tokens[0][1].strip()
        self.next_token()  # drop varName
        sym_kind = self.tables.kind_of(var_name)
        sym_idx = self.tables.index_of(var_name)

        if self.tokens[1][1].strip() == '[': #TODO some arr stuff
            self.next_token() # [
            self.compile_expression() 
            self.next_token()  # ]            

        self.next_token()  # drop =
        self.compile_expression()  # expression
        self.next_token()  # drop ;
        out_vm = VMWriter.write_pop(sym_kind, sym_idx)
        self.write_vm(out_vm)

    def compile_do(self):
        """
        get Method call info, call expression list
        """
        self.next_token()  # drop do
        while self.tokens[0][1].strip() != ';':
            if self.tokens[0][1].strip() == '(':
                self.next_token()  # drop ()
                self.compile_expression_list()
            elif self.tokens[0][1].strip() == ')':
                self.next_token()  # drop ()
            elif self.tokens[1][1].strip() == '.':
                out_vm  = VMWriter.write_push("local", 0)
                self.write_vm(out_vm)
                self.compile_expression_list()
        # out_vm, tokens = self.compile_subroutine_call(out_vm, tokens)
        self.next_token()  # drop ;
        out_vm = "pop temp 0\n"
        self.write_vm(out_vm)

    def compile_while(self):
        out_vm =VMWriter.write_label(f"WHILE_EXP{self.label_end}")
        self.write_vm(out_vm)
        self.next_token()  # drop while
        self.next_token()  # drop (
        self.compile_expression()
        self.next_token()  # drop )
        out_vm = VMWriter.write_arithmetic("not")
        self.write_vm(out_vm)
        out_vm = VMWriter.write_if(f"WHILE_EXP{self.label_end}")
        self.write_vm(out_vm)
        self.next_token()  # drop {
        self.in_statements = False  # risky flag flipping
        self.compile_statements()  # statement
        self.in_statements = True  # risky flag flipping
        self.next_token()  # drop }

        out_vm = VMWriter.write_goto(f"WHILE_EXP{self.label_end}")
        self.write_vm(out_vm)
        out_vm = VMWriter.write_label(f"WHILE_END{self.label_end}")
        self.write_vm(out_vm)

        self.label_end = self.label_end + 1

    def compile_return(self):
        self.next_token()  # drop return

        while self.tokens[0][1].strip() != ';':
            self.compile_expression()

        self.next_token()  # ;
        out_vm = VMWriter.write_return()  # TODO void?
        self.write_vm(out_vm)

    def compile_if(self):
        self.label_end = self.label_end + 1
        self.next_token()  # drop while
        self.next_token()  # drop (
        self.compile_expression()
        self.next_token()  # drop )
        out_vm = VMWriter.write_if(f"IF_TRUE{self.label_end}")
        self.write_vm(out_vm)
        out_vm = VMWriter.write_goto(f"IF_FALSE{self.label_end}")
        self.write_vm(out_vm)
        out_vm = VMWriter.write_label(f"IF_TRUE{self.label_end}")
        self.write_vm(out_vm)
        self.next_token()  # drop {
        self.in_statements = False  # risky flag flipping
        self.compile_statements()  # statement
        self.in_statements = True  # risky flag flipping
        self.next_token()  # drop }
        out_vm = VMWriter.write_goto(f"END{self.label_end}")
        self.write_vm(out_vm)
        out_vm = VMWriter.write_label(f"IF_FALSE{self.label_end}")
        self.write_vm(out_vm)
        if self.tokens[0][1].strip() == "else":
            self.next_token()  # drop else
            self.next_token()  # drop braket
            self.in_statements = False  # risky flag flipping
            self.compile_statements()  # statement
            self.in_statements = True  # risky flag flipping
            self.next_token()  # drop braket
        out_vm = VMWriter.write_label(f"END{self.label_end}")
        self.write_vm(out_vm)


    def compile_expression(self):
        if self.tokens[0][1].strip() == '(':
            self.next_token()  # drop (
            self.compile_expression()
            self.next_token()  # drop )
        else:
            self.compile_term()
        if self.tokens[0][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            token = self.tokens[0][1].strip()
            self.next_token()  # drop token
            self.compile_term()
            if token == '/':
                out_vm = VMWriter.write_call('Math.divide', 2)
                self.write_vm(out_vm)
            elif token == '*':
                out_vm = VMWriter.write_call('Math.multiply', 2)
                self.write_vm(out_vm)
            else:
                out_vm = VMWriter.write_arithmetic(math_ops[token])
                self.write_vm(out_vm)

    def compile_expression_list(self):
        self.args = 0
        while self.tokens[0][1].strip() not in [';',')']:
            if self.tokens[0][1].strip() == ',':
                self.next_token()  # drop ,
            else:
                self.args = self.args + 1
                self.compile_expression()

    def compile_term(self):
        token = self.tokens[0][1].strip()
        tag = self.tokens[0][0].strip()
        if tag == 'symbol':
            if token == '(':
                self.nested_expression = True
                self.next_token()  # drop (
                self.compile_expression()
                self.next_token()  # drop )
                self.nested_expression = False
            elif token in ['-', '~']:
                self.next_token()  # drop symbol
                self.compile_term()
                if token == '-':
                    out_vm = VMWriter.write_arithmetic('neg')
                    self.write_vm(out_vm)
                else:
                    out_vm = VMWriter.write_arithmetic('not')
                    self.write_vm(out_vm)
        elif tag == 'integerConstant':
            out_vm = VMWriter.write_push("constant", token)
            self.write_vm(out_vm)
            self.next_token()
        elif tag == 'stringConstant':
            out_vm = VMWriter.write_push('constant', len(token))  # more work to understand here
            self.write_vm(out_vm)
            out_vm = VMWriter.write_call('String.new', 1)
            self.write_vm(out_vm)
            for c in token:
                out_vm = VMWriter.write_push('constant', ord(c))
                self.write_vm(out_vm)
                out_vm = VMWriter.write_call('String.appendChar', 2)
                self.write_vm(out_vm)
            self.next_token()

        elif tag == 'keyword':
            if token == "true":
                out_vm = VMWriter.write_push("constant", 0)
                self.write_vm(out_vm)
                out_vm = VMWriter.write_arithmetic("not")
                self.write_vm(out_vm)
            if token in ["false", 'null']:
                out_vm = VMWriter.write_push("constant", 0)
                self.write_vm(out_vm)
            elif token == 'this':
                out_vm = VMWriter.write_push("pointer", 0)
                self.write_vm(out_vm)
            self.next_token()

        elif self.tokens[0][0] == 'identifier':
            idx = self.tables.index_of(token)
            id = self.tokens[0][1].strip()  # identifier
            self.next_token()
            if  self.tokens[0][1].strip() == '[':
                self.next_token()  #  [
                self.compile_expression()
                self.next_token()  #  ]
                vm_out = VMWriter.write_push(token, idx) #iffy TODO
                self.write_vm(out_vm)
                vm_out = VMWriter.write_arithmetic("add")
                self.write_vm(out_vm)
            elif self.tokens[0][1].strip() == '(':
                self.next_token()  #  (
                out_vm = VMWriter.write_push('pointer', 0)
                self.write_vm(out_vm)
                self.compile_expression()
                
                nargs = self.args + 1
                self.next_token()  #  )
                out_vm = VMWriter.write_call(f"{self.class_name}.{id}", nargs)
                self.write_vm(out_vm)

            elif self.tokens[0][1].strip() == '.':
                
                self.next_token()  # drop '.'
                id = f"{id}.{self.tokens[0][1].strip()}"
                self.next_token()  # drop identifier
                self.next_token()  # drop '('
                self.compile_expression_list()

                out_vm = VMWriter.write_call(id, self.args)
                self.write_vm(out_vm)
                self.next_token()  # drop')'

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
        # create list of tags and tokens
        for child in root:
            self.tokens.append([child.tag,child.text])

        while len(self.tokens) > 1:
            self.token_handler()

        return self.vm_out