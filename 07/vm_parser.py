def strip(vm):
    instructions = []
    for i in vm.read().splitlines():
        if len(i) > 0:
            if i[0] != '/' and i[1] !='/':
                v = filter_comment(i)
                instructions.append(v)
    return instructions            

def filter_comment(line):
    i = line.split('//')
    return i[0].strip()