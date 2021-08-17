import xml.etree.ElementTree as ET
in_expressions = False
in_statements = False

def compile_class_var_dec(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_subroutine_dec(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_parameter_list(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_subroutine_body(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_var_dec(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_statements(out_xml, tokens, depth):
    return out_xml, tokens, depth

def compile_let(out_xml, tokens, depth):
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

def compile_class(out_xml, tokens, depth):
    out_xml = out_xml + f"{tabs(depth)}<class>\n"  

    depth = depth + 1
    while tokens[0][1] != ' } ':
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)
        tokens.pop(0)

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
    tag,token = current[0],current[1]
    if token in non_terminal:
        out_xml, tokens, depth = non_terminal[token](out_xml, tokens, depth)
    else:
        out_xml = f"{tabs(depth)}<{tag}>{token}</{tag}>\n"    
    return out_xml, tokens, depth


def Engine(xml_in):
    root = ET.fromstring(xml_in)
    out_xml=""
    depth=0
    #create list of tags and tokens
    tokens = []
    for child in root:
        tokens.append([child.tag,child.text])

    while len(tokens) > 0:
        
        out_xml, tokens, depth = token_handler(out_xml, tokens, depth)
        tokens.pop(0)
    print(out_xml)    
    return out_xml    

def tabs(depth):
    tab = ""
    while depth > 0:
        tab = tab + "  "  
    return tab              

   