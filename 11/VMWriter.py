def write_push(segment, index):
    return f"push {segment} {index}\n"

def write_pop(segment, index):
    return

def write_arithmetic(command):
    return

def write_label(label):
    return

def write_goto(label):
    return

def write_if(label):
    return

def write_call(name, n_args):
    return f"call {name} {n_args}\n"

def write_function(name, n_vars):
    return f"function {name} {n_vars}\n"

def write_return():
    return "push constant 0\nreturn"