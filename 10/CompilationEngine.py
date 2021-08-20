import xml.etree.ElementTree as ET

class CompilationEngine:
    def __init__(self, xml_in):
        self.in_statements = False
        self.nested_expression = False
        self.xml_in = xml_in

    def compile_expression_list(self, out_xml, tokens, depth): 
        out_xml = out_xml + f"{self.tabs(depth)}<expressionList>\n"
        depth = depth+1 

        while tokens[0][1].strip() not in [';', ')']:
            out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)
            if tokens[0][1].strip() == ',':
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #,

        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</expressionList>\n"
        return out_xml, tokens, depth

    def compile_term(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<term>\n"
        depth = depth+1
        if tokens[0][1].strip() == '(':
            self.nested_expression = True
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)   # [,()
            out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)   # ],)
            self.nested_expression = False
        elif tokens[0][0] in ('integerConstant', 'stringConstant', 'keyword'):
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
        elif tokens[0][0] == 'identifier':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # identifier
            if tokens[0][1].strip() in ['[', '(']:
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # [,()
                out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ],)
            elif tokens[0][1].strip() == '.':
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # '.'
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # identifier
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # '('
                out_xml, tokens, depth = self.compile_expression_list(out_xml, tokens, depth)                
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ')'
            elif tokens[0][1].strip() == '(':
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # (
                out_xml, tokens, depth = self.compile_expression_list(out_xml, tokens, depth)
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # )
        elif tokens[0][1].strip() in ['-', '~']:

            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
            out_xml, tokens, depth = self.compile_term(out_xml, tokens, depth)
        else:
            while tokens[0][1].strip() != ';':          
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)   
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</term>\n"
        return out_xml, tokens, depth    

    def compile_expression(self, out_xml, tokens, depth):
        terms = ['identifier', 'integerConstant', 'stringConstant']
        out_xml = out_xml + f"{self.tabs(depth)}<expression>\n"
        depth = depth+1
        while tokens[0][1].strip() not in [';', ')', ',', ']']:
            if tokens[0][0] == 'identifier' and tokens[1][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                out_xml, tokens, depth = self.compile_term(out_xml, tokens, depth)
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
            elif tokens[0][1].strip() in ['-', '~'] and tokens[1][0] in terms and self.nested_expression is True:
                out_xml, tokens, depth = self.compile_term(out_xml, tokens, depth)
            elif tokens[0][1].strip() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
            else:
                out_xml, tokens, depth = self.compile_term(out_xml, tokens, depth)
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</expression>\n"
        return out_xml, tokens, depth    

    def if_while_help(self, out_xml, tokens, depth):
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)  # if/while
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # (
        out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)  # expression
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # )
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) # {
        self.in_statements = False  # risky flag flipping
        out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth)  # statement
        self.in_statements = True  # risky flag flipping
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # }
        return out_xml, tokens, depth
        
    def compile_while(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<whileStatement>\n"
        depth = depth+1
        out_xml, tokens, depth = self.if_while_help(out_xml, tokens, depth)
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</whileStatement>\n"
        return out_xml, tokens, depth

    def compile_if(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<ifStatement>\n"
        depth = depth+1
        out_xml, tokens, depth = self.if_while_help(out_xml, tokens, depth)
        if tokens[0][1].strip() == "else":
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # else
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) # {
            self.in_statements = False  # risky flag flipping
            out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth)  # statement
            self.in_statements = True  # risky flag flipping
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) # }

        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</ifStatement>\n"
        return out_xml, tokens, depth    

    def compile_let(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<letStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)  # let

        if tokens[1][1].strip() == '[':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # varName
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # [
            out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ]
        else:
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # varName
            
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # =
        out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth)  # expression
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ;
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</letStatement>\n"
       
        return out_xml, tokens, depth    

    def compile_return(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<returnStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)  # return

        while tokens[0][1].strip() != ';':
            out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth) 

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ;
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</returnStatement>\n"
        return out_xml, tokens, depth    

    def compile_do(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<doStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)  # do
        while tokens[0][1].strip() != ';':
            if tokens[0][1].strip() == '(':
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
                out_xml, tokens, depth = self.compile_expression_list(out_xml, tokens, depth)
            elif tokens[0][1].strip() != ';':
                out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # )?

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  # ;
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</doStatement>\n"
        return out_xml, tokens, depth    

    def compile_statements(self, out_xml, tokens, depth):
        """
        check if we're in a statements block or not to initialize or not 
        """
        if not self.in_statements:
            self.in_statements = True
            out_xml = out_xml + f"{self.tabs(depth)}<statements>\n"
            depth = depth+1
        statements_list = ['let', 'if', 'while', 'do', 'return']

        while tokens[0][1].strip() in statements_list:
            token = tokens[0][1].strip()
            if token == 'let':
                out_xml, tokens, depth = self.compile_let(out_xml, tokens, depth)
            elif token == 'if':
                out_xml, tokens, depth = self.compile_if(out_xml, tokens, depth)
            elif token == 'return':
                out_xml, tokens, depth = self.compile_return(out_xml, tokens, depth)
            elif token == 'do':
                out_xml, tokens, depth = self.compile_do(out_xml, tokens, depth)
            elif token == 'while':    
                out_xml, tokens, depth = self.compile_while(out_xml, tokens, depth)


        self.in_statements = False
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</statements>\n"
        return out_xml, tokens, depth

    def compile_var_dec(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<varDec>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth) 

        while tokens[0][1].strip() != ';':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) 
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</varDec>\n"
        return out_xml, tokens, depth

    def compile_subroutine_body(self, out_xml, tokens, depth):
        """
        set first parameterList and call token handler for open bracket
        iterate through remaining tags until we find closing bracket
        then wrap up
        """
        out_xml = out_xml + f"{self.tabs(depth)}<subroutineBody>\n"
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  
        
        depth = depth+1
        
        while tokens[0][1].strip() != '}':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) 

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) 
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</subroutineBody>\n"
        return out_xml, tokens, depth    

    def compile_parameter_list(self, out_xml, tokens, depth):
        """
        set first parameterList and call token handler for open paren
        iterate through remaining tags until we find closing paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)  
        out_xml = out_xml + f"{self.tabs(depth)}<parameterList>\n"
        depth = depth+1
        
        while tokens[0][1].strip() != ')':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) 

        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</parameterList>\n"
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) 
        return out_xml, tokens, depth

    def compile_subroutine_dec(self, out_xml, tokens, depth):
        """
        set first subroutineDec and keyword tags, pop first time
        iterate through remaining tags until we find opening paren,
        then call param list
        then call subroutine body
        then wrap up
        """
        out_xml = out_xml + f"{self.tabs(depth)}<subroutineDec>\n"
        depth=depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)  

        while tokens[0][1].strip() != '(':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)

        out_xml, tokens, depth = self.compile_parameter_list(out_xml, tokens, depth)  # todo
        out_xml, tokens, depth = self.compile_subroutine_body(out_xml, tokens, depth)
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</subroutineDec>\n"
        return out_xml, tokens, depth

    def compile_class_var_dec(self, out_xml, tokens, depth):
        """
        set first classVarDec and keyword tags, pop first time
        iterate through remaining tags until we find semicolon
        then wrap things up
        """
        out_xml = out_xml + f"{self.tabs(depth)}<classVarDec>\n"
        depth=depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth)

        while tokens[0][1].strip() != ';':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
        depth=depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</classVarDec>\n"
        return out_xml, tokens, depth   

    def compile_class(self, out_xml, tokens, depth):
        """
        set first class and keyword tags, pop first time
        iterate through remaining tags until we find closing braket
        then wrap things up
        """
        out_xml = out_xml + f"{self.tabs(depth)}<class>\n"
        depth=depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth) 

        while tokens[0][1].strip() != '}':
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)        

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
        depth=depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</class>\n"
        return out_xml, tokens, depth    

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

    def token_handler(self, out_xml, tokens, depth):
        current = tokens[0]
        tag, token = current[0], current[1].strip()

        if token in self.non_terminal:
            if token == 'class':
                out_xml, tokens, depth = self.compile_class(out_xml, tokens, depth)
            elif token in ['static', 'field']:
                out_xml, tokens, depth = self.compile_class_var_dec(out_xml, tokens, depth)
            elif token in ['constructor', 'function', 'method']:
                out_xml, tokens, depth = self.compile_subroutine_dec(out_xml, tokens, depth)
            elif token == 'var':
                out_xml, tokens, depth = self.compile_var_dec(out_xml, tokens, depth)
            elif token in ['let', 'if', 'while', 'do', 'return']:
                out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth)
            
        else:
            if token == '<':
                sym = '&lt;'
            elif token == '>':
                sym = '&gt;'
            elif token == '&':
                sym = '&amp;'
            else:
                sym = token
            out_xml = out_xml + f"{self.tabs(depth)}<{tag}> {sym} </{tag}>\n"
            tokens.pop(0) 

        return out_xml, tokens, depth

    def non_terminal_keyword(self, out_xml, tokens, depth):
        current = tokens[0]
        tag,token = current[0],current[1].strip()
        
        out_xml = out_xml + f"{self.tabs(depth)}<{tag}>{current[1]}</{tag}>\n"
        tokens.pop(0) 
        return out_xml, tokens

    def Engine(self):
        root = ET.fromstring(self.xml_in)
        out_xml = ""
        depth = 0
        # create list of tags and tokens
        tokens = []
        for child in root:
            tokens.append([child.tag,child.text])

        while len(tokens) > 1:
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
        
        return out_xml    

    def tabs(self, depth):
        tab_num = depth
        tab = ""
        while tab_num > 0:
            tab = tab + "  "
            tab_num = tab_num-1
        return tab
