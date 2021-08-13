symbols = ['{', '}', '(', ')', '[', ']', '. ', ', ', '; ',
           '+', '-', '*', '/', '&', ',', '<', '>', '=', '~']
keywords = ['class', 'constructor', 'function',
            'method', 'field', 'static', 'var', 'int',
            'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else',
            'while', 'return']

def tokenize(in_jack):
    stripped_jack = strip(in_jack)
    tokens = '<tokens> \n'
    for line in stripped_jack:
        tokens = tokens + parse_tokens(line)
    tokens = tokens + '</tokens>'
    return tokens

def parse_tokens(line):
    tokens = ""
    token = ""
    token_type = ""
    for item in line:
        # if token_type == "Identifier" and not item.isalnum() and item != "_" and token in keywords:
        #     tokens = tokens + '<keyword> {token} </keyword>\n'
        #     token_type, token = ""
        if item == '"' and token_type != "String":
            
            token_type = "String"
            
        elif item == '"' and token_type == "String":
            print(item)
            tokens = tokens + "<stringConstant> {token} </stringConstant>\n"
            token_type, token = ""
        elif token_type == "String":
            
            token = token + item
        # elif item in symbols:
        #     tokens = tokens + f"<symbol>{item}</symbol>\n"
        # elif item.isnumeric() and token_type != "Identifier":
        #     token = token + item
        #     token_type = "Integer"
        # elif token_type == "Integer":
        #     tokens = tokens + '<integerConstant> {token} </integerConstant>\n'
        #     token_type, token = ""
        # elif item.isalnum() or item == "_":
        #     token = token + item
        #     token_type = "Identifier"
        # elif token_type == "Identifier":
        #     tokens = tokens + '<identifier> {token} </identifier>\n'
        #     token_type, token = ""
    return tokens

def strip(jack):
    """remove white space and comments"""
    code = ""
    comment_block = False
    for i in jack.read().splitlines():
        line = i.strip()  # clean whitespace
        if len(line) == 0:
            continue
        elif len(line) > 0 and line[0] == '*' and comment_block:
            continue
        elif len(line) > 0 and not comment_block:
            comment_block = False
        if len(line) > 1 and line[0] == '/' and line[1] == '/':
            continue
        elif len(line) > 1 and line[0] == '/' and line[1] == '*':
            comment_block = True
        else:
            v = filter_comment(line)
            code = code + v + '\n'
    return code


def filter_comment(line):
    """filter comments"""
    i = line.split('//')
    return i[0].strip()
