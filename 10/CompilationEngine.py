import xml.etree.ElementTree as ET
class CompilationEngine:
    def __init__(self, xml_in):
        self.in_expressions = False
        self.in_statements = False
        self.xml_in = xml_in

    def compile_statements(self, out_xml, tokens, depth):
        return out_xml, tokens, depth

    def compile_do(self, out_xml, tokens, depth):
        return out_xml, tokens, depth

    def compile_while(self, out_xml, tokens, depth):
        return out_xml, tokens, depth

    def compile_term(self, out_xml, tokens, depth):
        return out_xml, tokens, depth

    def compile_expression(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<expression>\n"
        depth = depth+1
        out_xml = out_xml + f"{self.tabs(depth)}<term>\n"
        depth = depth+1

        while tokens[0][1].strip() not in [';', ')']:
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)

        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</term>\n"
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</expression>\n"
        return out_xml, tokens, depth    

    def compile_if(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<ifStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth) #if
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #(
        out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth) #expression
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #)
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #{
        self.in_statements = False #risky flag flipping
        out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth) #statement
        self.in_statements = True #risky flag flipping
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #}

        if tokens[0][1].strip() == "else":
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #else
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #{
            self.in_statements = False #risky flag flipping
            out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth) #statement
            self.in_statements = True #risky flag flipping
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #}

        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</ifStatement>\n"
        return out_xml, tokens, depth    

    def compile_let(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<letStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth) #let

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #varName
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #=

        out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth) #expression
                
        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #;
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</letStatement>\n"
        return out_xml, tokens, depth    

    def compile_return(self, out_xml, tokens, depth):
        out_xml = out_xml + f"{self.tabs(depth)}<returnStatement>\n"
        depth = depth+1
        out_xml, tokens = self.non_terminal_keyword(out_xml, tokens, depth) #return

        while tokens[0][1].strip() != ';':
            out_xml, tokens, depth = self.compile_expression(out_xml, tokens, depth) 

        out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth) #;
        depth = depth-1
        out_xml = out_xml + f"{self.tabs(depth)}</returnStatement>\n"
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
            if token == 'if':
                out_xml, tokens, depth = self.compile_if(out_xml, tokens, depth)
            if token == 'return':
                out_xml, tokens, depth = self.compile_return(out_xml, tokens, depth)



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

        out_xml, tokens, depth = self.compile_parameter_list(out_xml, tokens, depth) #todo
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

    non_terminal = {
        'class': compile_class,
        'static': compile_class_var_dec,
        'field': compile_class_var_dec,
        'constructor': compile_subroutine_dec,
        'function': compile_subroutine_dec,
        'method': compile_subroutine_dec,
        'var': compile_var_dec,
        'let': compile_statements,
        'if': compile_statements,
        'while': compile_statements,
        'return': compile_statements,
        'do': compile_statements
        # '': compile_expression_list, #may need speical handing for expressions
        # '':expression,
        # '': compile_term
    }
    statements_list ={
        'let': compile_let, #may need special handling for statements
        'if': compile_if,
        'while': compile_while,
        'return': compile_return,
        'do': compile_do    
    }

    def token_handler(self, out_xml, tokens, depth):
        current = tokens[0]
        tag,token = current[0],current[1].strip() #strip white space from around token
        
        if token in self.non_terminal:
            if token == 'class':
                out_xml, tokens, depth = self.compile_class(out_xml, tokens, depth)
            elif token in ['static', 'field']:
                out_xml, tokens, depth = self.compile_class_var_dec(out_xml, tokens, depth)
            elif token in ['constructor', 'function','method']:
                out_xml, tokens, depth = self.compile_subroutine_dec(out_xml, tokens, depth)
            elif token == 'var':
                out_xml, tokens, depth = self.compile_var_dec(out_xml, tokens, depth)
            elif token in ['let', 'if','while', 'do', 'return']:
                out_xml, tokens, depth = self.compile_statements(out_xml, tokens, depth)
            
        else:
            out_xml = out_xml + f"{self.tabs(depth)}<{tag}> {token} </{tag}>\n"   
            tokens.pop(0) 

        return out_xml, tokens, depth

    def non_terminal_keyword(self, out_xml, tokens, depth):
        current = tokens[0]
        tag,token = current[0],current[1].strip()
        
        out_xml = out_xml + f"{self.tabs(depth)}<{tag}> {token} </{tag}>\n"   
        tokens.pop(0) 
        return out_xml, tokens

    def Engine(self):
        root = ET.fromstring(self.xml_in)
        out_xml=""
        depth=0
        #create list of tags and tokens
        tokens = []
        for child in root:
            tokens.append([child.tag,child.text])

        while len(tokens) > 1:
            out_xml, tokens, depth = self.token_handler(out_xml, tokens, depth)
        
        return out_xml    

    def tabs(self, depth):
        tabnum = depth
        tab = ""
        while tabnum > 0:
            tab = tab + "  "  
            tabnum = tabnum-1
        return tab              