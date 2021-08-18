import xml.etree.ElementTree as ET
in_expressions = False
in_statements = False

def compile_statements(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_if(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_do(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_while(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_return(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_term(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_expression_list(out_xml, tokens, depth):
    return out_xml, tokens, depth 

def compile_let(out_xml, tokens, depth):
    
    return out_xml, tokens, depth    

def compile_var_dec(out_xml, tokens, depth):
    out_xml = out_xml + f"{tabs(depth)}<varDec>\n"
    depth = depth+1
    out_xml, tokens = non_terminal_keyword(out_xml, tokens, depth) 

    while tokens[0][1].strip() != ';':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)

    out_xml, tokens, depth = token_handler(out_xml, tokens, depth) 
    depth = depth-1
    out_xml = out_xml + f"{tabs(depth)}</varDec>\n"    

    return out_xml, tokens, depth

def compile_subroutine_body(out_xml, tokens, depth):
    """
    set first parameterList and call token handler for open bracket
    iterate through remaining tags until we find closing bracket
    then wrap up
    """
    out_xml = out_xml + f"{tabs(depth)}<subroutineBody>\n"
    out_xml, tokens, depth = token_handler(out_xml, tokens, depth)  
    
    depth = depth+1
    
    while tokens[0][1].strip() != '}':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth) 


    out_xml, tokens, depth = token_handler(out_xml, tokens, depth) 
    depth = depth-1
    out_xml = out_xml + f"{tabs(depth)}</subroutineBody>\n"
    return out_xml, tokens, depth    

def compile_parameter_list(out_xml, tokens, depth):
    """
    set first parameterList and call token handler for open paren
    iterate through remaining tags until we find closing paren,
    then call param list
    then call subroutine body
    then wrap up
    """
    out_xml, tokens, depth = token_handler(out_xml, tokens, depth)  
    out_xml = out_xml + f"{tabs(depth)}<parameterList>\n"
    depth = depth+1
    
    while tokens[0][1].strip() != ')':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth) 

    depth = depth-1
    out_xml = out_xml + f"{tabs(depth)}</parameterList>\n"
    out_xml, tokens, depth = token_handler(out_xml, tokens, depth) 
    return out_xml, tokens, depth

def compile_subroutine_dec(out_xml, tokens, depth):
    """
    set first subroutineDec and keyword tags, pop first time
    iterate through remaining tags until we find opening paren,
    then call param list
    then call subroutine body
    then wrap up
    """
    out_xml = out_xml + f"{tabs(depth)}<subroutineDec>\n"  
    depth=depth+1
    out_xml, tokens = non_terminal_keyword(out_xml, tokens, depth)  

    while tokens[0][1].strip() != '(':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)

    out_xml, tokens, depth = compile_parameter_list(out_xml, tokens, depth) #todo
    out_xml, tokens, depth = compile_subroutine_body(out_xml, tokens, depth)
    depth = depth-1
    out_xml = out_xml + f"{tabs(depth)}</subroutineDec>\n"
    return out_xml, tokens, depth

def compile_class_var_dec(out_xml, tokens, depth):
    """
    set first classVarDec and keyword tags, pop first time
    iterate through remaining tags until we find semicolon
    then wrap things up
    """
    out_xml = out_xml + f"{tabs(depth)}<classVarDec>\n"  
    depth=depth+1
    out_xml, tokens = non_terminal_keyword(out_xml, tokens, depth)

    while tokens[0][1].strip() != ';':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)

    out_xml, tokens, depth = token_handler(out_xml, tokens, depth)
    depth=depth-1
    out_xml = out_xml + f"{tabs(depth)}</classVarDec>\n"
    return out_xml, tokens, depth   

def compile_class(out_xml, tokens, depth):
    """
    set first class and keyword tags, pop first time
    iterate through remaining tags until we find closing braket
    then wrap things up
    """
    out_xml = out_xml + f"{tabs(depth)}<class>\n"  
    depth=depth+1
    out_xml, tokens = non_terminal_keyword(out_xml, tokens, depth) 

    while tokens[0][1].strip() != '}':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)        

    out_xml, tokens, depth = token_handler(out_xml, tokens, depth)
    depth=depth-1
    out_xml = out_xml + f"{tabs(depth)}</class>\n"
    return out_xml, tokens, depth    

non_terminal = {
    'class': compile_class,
    'static': compile_class_var_dec,
    'field': compile_class_var_dec,
    'constructor': compile_subroutine_dec,
    'function': compile_subroutine_dec,
    'method': compile_subroutine_dec,
    # '' : compile_parameter_list,
    # '':compile_subroutine_body,
    'var': compile_var_dec,
    # '': compile_statements,
    # 'let': compile_let, #may need special handling for statements
    # 'if': compile_if,
    # 'while': compile_while,
    # 'return': compile_return,
    # '': compile_expression_list, #may need speical handing for expressions
    # '':expression,
    # '': compile_term
}
def token_handler(out_xml, tokens, depth):
    current = tokens[0]
    tag,token = current[0],current[1].strip() #strip white space from around token
    
    if token in non_terminal:
        out_xml, tokens, depth = non_terminal[token](out_xml, tokens, depth)
    else:
        out_xml = out_xml + f"{tabs(depth)}<{tag}> {token} </{tag}>\n"   
        tokens.pop(0) 

    return out_xml, tokens, depth

def non_terminal_keyword(out_xml, tokens, depth):
    current = tokens[0]
    tag,token = current[0],current[1].strip()
    
    out_xml = out_xml + f"{tabs(depth)}<{tag}> {token} </{tag}>\n"   
    tokens.pop(0) 
    return out_xml, tokens

def Engine(xml_in):
    root = ET.fromstring(xml_in)
    out_xml=""
    depth=0
    #create list of tags and tokens
    tokens = []
    for child in root:
        tokens.append([child.tag,child.text])

    while len(tokens) > 1:
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)
    
    return out_xml    

def tabs(depth):
    tabnum = depth
    tab = ""
    while tabnum > 0:
        tab = tab + "  "  
        tabnum = tabnum-1
    return tab              

   