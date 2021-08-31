import xml.etree.ElementTree as ET
from SymbolTable import SymbolTable
class CompilationEngine:
    def __init__(self, xml_in):
        self.in_statements = False
        self.nested_expression = False
        self.xml_in = xml_in
        self.tables = SymbolTable()
        self.class_name = ""

    def compile_expression_list(self, out_vm, tokens): 
        # out_vm = out_vm + f"{self.tabs(depth)}<expressionList>\n"
        

        while tokens[0][1].strip() not in [';', ')']:
            out_vm, tokens = self.compile_expression(out_vm, tokens)
            if tokens[0][1].strip() == ',':
                out_vm, tokens = self.token_handler(out_vm, tokens) #,

      
        # out_vm = out_vm + f"{self.tabs(depth)}</expressionList>\n"
        return out_vm, tokens

    def compile_term(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<term>\n"
       
        if tokens[0][1].strip() == '(':
            self.nested_expression = True
            out_vm, tokens = self.token_handler(out_vm, tokens)   # [,()
            out_vm, tokens = self.compile_expression(out_vm, tokens)
            out_vm, tokens = self.token_handler(out_vm, tokens)   # ],)
            self.nested_expression = False
        elif tokens[0][0] in ('integerConstant', 'stringConstant', 'keyword'):
            out_vm, tokens = self.token_handler(out_vm, tokens)
        elif tokens[0][0] == 'identifier':
            out_vm, tokens = self.token_handler(out_vm, tokens)  # identifier
            if tokens[0][1].strip() in ['[', '(']:
                out_vm, tokens = self.token_handler(out_vm, tokens)  # [,()
                out_vm, tokens = self.compile_expression(out_vm, tokens)
                out_vm, tokens = self.token_handler(out_vm, tokens)  # ],)
            elif tokens[0][1].strip() == '.':
                out_vm, tokens = self.token_handler(out_vm, tokens)  # '.'
                out_vm, tokens = self.token_handler(out_vm, tokens)  # identifier
                out_vm, tokens = self.token_handler(out_vm, tokens)  # '('
                out_vm, tokens = self.compile_expression_list(out_vm, tokens)                
                out_vm, tokens = self.token_handler(out_vm, tokens)  # ')'
            elif tokens[0][1].strip() == '(':
                out_vm, tokens = self.token_handler(out_vm, tokens)  # (
                out_vm, tokens = self.compile_expression_list(out_vm, tokens)
                out_vm, tokens = self.token_handler(out_vm, tokens)  # )
        elif tokens[0][1].strip() in ['-', '~']:

            out_vm, tokens = self.token_handler(out_vm, tokens)
            out_vm, tokens = self.compile_term(out_vm, tokens)
        else:
            while tokens[0][1].strip() != ';':          
                out_vm, tokens = self.token_handler(out_vm, tokens)   
 
        # out_vm = out_vm + f"{self.tabs(depth)}</term>\n"
        return out_vm, tokens    

    def compile_expression(self, out_vm, tokens):
        terms = ['identifier', 'integerConstant', 'stringConstant']
        # out_vm = out_vm + f"{self.tabs(depth)}<expression>\n"
        
        while tokens[0][1].strip() not in [';', ')', ',', ']']:
            if tokens[0][0] == 'identifier' and tokens[1][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                out_vm, tokens = self.compile_term(out_vm, tokens)
                out_vm, tokens = self.token_handler(out_vm, tokens)
            elif tokens[0][1].strip() in ['-', '~'] and tokens[1][0] in terms and self.nested_expression is True:
                out_vm, tokens = self.compile_term(out_vm, tokens)
            elif tokens[0][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                out_vm, tokens = self.token_handler(out_vm, tokens)
            else:
                out_vm, tokens = self.compile_term(out_vm, tokens)
        
        # out_vm = out_vm + f"{self.tabs(depth)}</expression>\n"
        return out_vm, tokens    

    def if_while_help(self, out_vm, tokens):
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)  # if/while
        out_vm, tokens = self.token_handler(out_vm, tokens)  # (
        out_vm, tokens = self.compile_expression(out_vm, tokens)  # expression
        out_vm, tokens = self.token_handler(out_vm, tokens)  # )
        out_vm, tokens = self.token_handler(out_vm, tokens) # {
        self.in_statements = False  # risky flag flipping
        out_vm, tokens = self.compile_statements(out_vm, tokens)  # statement
        self.in_statements = True  # risky flag flipping
        out_vm, tokens = self.token_handler(out_vm, tokens)  # }
        return out_vm, tokens
        
    def compile_while(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<whileStatement>\n"
      
        out_vm, tokens = self.if_while_help(out_vm, tokens)
     
        # out_vm = out_vm + f"{self.tabs(depth)}</whileStatement>\n"
        return out_vm, tokens

    def compile_if(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<ifStatement>\n"
    
        out_vm, tokens = self.if_while_help(out_vm, tokens)
        if tokens[0][1].strip() == "else":
            out_vm, tokens = self.token_handler(out_vm, tokens)  # else
            out_vm, tokens = self.token_handler(out_vm, tokens) # {
            self.in_statements = False  # risky flag flipping
            out_vm, tokens = self.compile_statements(out_vm, tokens)  # statement
            self.in_statements = True  # risky flag flipping
            out_vm, tokens = self.token_handler(out_vm, tokens) # }

       
        # out_vm = out_vm + f"{self.tabs(depth)}</ifStatement>\n"
        return out_vm, tokens    

    def compile_let(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<letStatement>\n"
        
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)  # let

        if tokens[1][1].strip() == '[':
            out_vm, tokens = self.token_handler(out_vm, tokens)  # varName
            out_vm, tokens = self.token_handler(out_vm, tokens)  # [
            out_vm, tokens = self.compile_expression(out_vm, tokens)
            out_vm, tokens = self.token_handler(out_vm, tokens)  # ]
        else:
            out_vm, tokens = self.token_handler(out_vm, tokens)  # varName
            
        out_vm, tokens = self.token_handler(out_vm, tokens)  # =
        out_vm, tokens = self.compile_expression(out_vm, tokens)  # expression
        out_vm, tokens = self.token_handler(out_vm, tokens)  # ;
       
        # out_vm = out_vm + f"{self.tabs(depth)}</letStatement>\n"
       
        return out_vm, tokens    

    def compile_return(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<returnStatement>\n"
       
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)  # return

        while tokens[0][1].strip() != ';':
            out_vm, tokens = self.compile_expression(out_vm, tokens) 

        out_vm, tokens = self.token_handler(out_vm, tokens)  # ;
     
        # out_vm = out_vm + f"{self.tabs(depth)}</returnStatement>\n"
        return out_vm, tokens    

    def compile_do(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<doStatement>\n"
      
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)  # do
        while tokens[0][1].strip() != ';':
            if tokens[0][1].strip() == '(':
                out_vm, tokens = self.token_handler(out_vm, tokens)
                out_vm, tokens = self.compile_expression_list(out_vm, tokens)
            elif tokens[0][1].strip() != ';':
                out_vm, tokens = self.token_handler(out_vm, tokens)  # )?

        out_vm, tokens = self.token_handler(out_vm, tokens)  # ;
      
        # out_vm = out_vm + f"{self.tabs(depth)}</doStatement>\n"
        return out_vm, tokens    

    def compile_statements(self, out_vm, tokens):
        """
        check if we're in a statements block or not to initialize or not 
        """
        if not self.in_statements:
            self.in_statements = True
            # out_vm = out_vm + f"{self.tabs(depth)}<statements>\n"
          
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
    
        # out_vm = out_vm + f"{self.tabs(depth)}</statements>\n"
        return out_vm, tokens

    def compile_class_var_dec(self, out_vm, tokens):
        """
        set first classVarDec and keyword tags, pop first time
        iterate through remaining tags until we find semicolon
        then wrap things up
        """
        # out_vm = out_vm + f"{self.tabs(depth)}<classVarDec>\n"
       
        sym_kind = tokens[0][1].strip()
        sym_type = tokens[1][1].strip() #boolean, int, etc. 

        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)
        
        while tokens[0][1].strip() != ';':
            if tokens[0][0] == 'identifier' and tokens[1][0] != 'identifier': #TODO this handles if an Object is the var type. Maybe not good enough?
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            out_vm, tokens = self.token_handler(out_vm, tokens)

        out_vm, tokens = self.token_handler(out_vm, tokens)
       
        # out_vm = out_vm + f"{self.tabs(depth)}</classVarDec>\n"
        return out_vm, tokens      

    def compile_var_dec(self, out_vm, tokens):
        # out_vm = out_vm + f"{self.tabs(depth)}<varDec>\n"

    
        sym_kind = 'local'
        sym_type = tokens[1][1].strip() #boolean, int, etc. 
        
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens) 
     
        while tokens[0][1].strip() != ';':
            if tokens[0][0] == 'identifier' and tokens[1][0] != 'identifier': #TODO this handles if an Object is the var type. Maybe not good enough?
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            out_vm, tokens = self.token_handler(out_vm, tokens)

        out_vm, tokens = self.token_handler(out_vm, tokens) 
     
        # out_vm = out_vm + f"{self.tabs(depth)}</varDec>\n"
        return out_vm, tokens

    def compile_subroutine_body(self, out_vm, tokens):
        """
        set first parameterList and call token handler for open bracket
        iterate through remaining tags until we find closing bracket
        then wrap up
        """
        # out_vm = out_vm + f"self.tabs(depth)}<subroutineBody>\n"
        out_vm, tokens = self.token_handler(out_vm, tokens)  

        
        while tokens[0][1].strip() != '}':
            out_vm, tokens = self.token_handler(out_vm, tokens) 

        out_vm, tokens = self.token_handler(out_vm, tokens) 
      
        # out_vm = out_vm + f"{self.tabs(depth)}</subroutineBody>\n"
        return out_vm, tokens    

    def compile_parameter_list(self, out_vm, tokens):
        """
        set first parameterList and call token handler for open paren
        iterate through remaining tags until we find closing paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        out_vm, tokens = self.token_handler(out_vm, tokens)  
        # out_vm = out_vm + f"{self.tabs(depth)}<parameterList>\n"
        
        sym_type = tokens[0][1].strip() #int, Object, etc.
        sym_kind = 'argument' 
        
        while tokens[0][1].strip() != ')':
            if tokens[0][0] == 'identifier':
                self.tables.define(tokens[0][1].strip(), sym_type, sym_kind)
            elif tokens[0][1].strip() == ',': #new parameter coming, look ahead for type
                sym_type = tokens[1][1].strip() #int, Object, etc.

            out_vm, tokens = self.token_handler(out_vm, tokens) 

  
        # out_vm = out_vm + f"{self.tabs(depth)}</parameterList>\n"
        out_vm, tokens = self.token_handler(out_vm, tokens) 
        return out_vm, tokens

    def compile_subroutine_dec(self, out_vm, tokens):
        """
        set first subroutineDec and keyword tags, pop first time
        iterate through remaining tags until we find opening paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        self.tables.start_subroutine()
        # out_vm = out_vm + f"{self.tabs(depth)}<subroutineDec>\n"
      
        if tokens[0][1].strip() == 'method':
            self.tables.define('this', self.class_name, 'argument')
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens)  
        
        while tokens[0][1].strip() != '(':
            out_vm, tokens = self.token_handler(out_vm, tokens)

        out_vm, tokens = self.compile_parameter_list(out_vm, tokens)  
        out_vm, tokens = self.compile_subroutine_body(out_vm, tokens)
    
        # out_vm = out_vm + f"{self.tabs(depth)}</subroutineDec>\n"

        return out_vm, tokens 

    def compile_class(self, out_vm, tokens):
        """
        set first class and keyword tags, pop first time
        iterate through remaining tags until we find closing braket
        then wrap things up
        """
        
        # out_vm = out_vm + f"{self.tabs(depth)}<class>\n"
  
        out_vm, tokens = self.non_terminal_keyword(out_vm, tokens) 
        self.class_name = tokens[0][1].strip()

        while tokens[0][1].strip() != '}':
            out_vm, tokens = self.token_handler(out_vm, tokens)        

        out_vm, tokens = self.token_handler(out_vm, tokens)
      
        # out_vm = out_vm + f"{self.tabs(depth)}</class>\n"
        
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
    statements_list ={
        'let': compile_let,  # todo - make array?
        'if': compile_if,
        'while': compile_while,
        'return': compile_return,
        'do': compile_do    
    }

    def token_handler(self, out_vm, tokens):
        current = tokens[0]
        tag, token = current[0], current[1].strip()

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
            
        else:
            if token == '<':
                sym = '&lt;'
            elif token == '>':
                sym = '&gt;'
            elif token == '&':
                sym = '&amp;'
            else:
                sym = token.strip()
            if tag == 'identifier':
                return #just to get rid of error
                # out_vm = out_vm + f"{self.tabs(depth)}<{tag}> {sym} {self.tables.type_of(sym)} {self.tables.kind_of(sym)} {self.tables.index_of(sym)}</{tag}>\n"
            # else: 
                # return   
                #  out_vm = out_vm + f"{self.tabs(depth)}<{tag}> {sym} </{tag}>\n"
            tokens.pop(0) 

        return out_vm, tokens

    def non_terminal_keyword(self, out_vm, tokens):
        current = tokens[0]
        tag,token = current[0],current[1].strip()
        
        # out_vm = out_vm + f"{self.tabs(depth)}<{tag}>{current[1]}</{tag}>\n"
        tokens.pop(0) 
        return out_vm, tokens

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

    # def tabs(self):
    #     # tab_num = depth
    #     tab = ""
    #     while tab_num > 0:
    #         tab = tab + "  "
    #         tab_num = tab_num-1
    #     return tab
