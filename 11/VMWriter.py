def write_push(segment, index):
    return f"push {segment} {index}\n"

def write_pop(segment, index):
    return  f"pop {segment} {index}\n"

def write_arithmetic(command):
    return f"{command}\n"

def write_label(label):
    return f"label {label}\n"

def write_goto(label):
    return f"goto {label}\n"

def write_if(label):
    return f"if-goto {label}\n"

def write_call(name, n_args):
    return f"call {name} {n_args}\n"

def write_function(name, n_vars):
    return f"function {name} {n_vars}\n"

def write_return():
    return "push constant 0\nreturn\n"