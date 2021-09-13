import Tokenizer
from CompilationEngine import CompilationEngine
import os, sys

if __name__ == "__main__":
    in_args = sys.argv[1:]

    if len(in_args) == 1 and os.path.isdir(in_args[0]):
        out_folder = in_args[0]+'\output'        
        for root, dirs, files in os.walk(in_args[0]):
            for file in files:
                if file.endswith('.jack'):
                    file_name = file.split(".")[0] #this gets the name of the file minus .jack 
                    file_in = open(f"{in_args[0]}\\{file}", "r")
                    tokenized_jack = Tokenizer.tokenize(file_in) 
                    e = CompilationEngine(tokenized_jack)
                    compiled_jack = e.Engine()
                    compilation_out=open(f"{out_folder}\\{file_name}.vm", "w")
                    compilation_out.write(compiled_jack)
