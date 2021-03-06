import Tokenizer
from CompilationEngine import CompilationEngine
import os

if __name__ == "__main__":
    in_folder1 =r'C:\Users\agilvarry\Documents\github\nand2tetris\10\Square'
    in_folder2=r'C:\Users\agilvarry\Documents\github\nand2tetris\10\ArrayTest'
    in_folder3=r'C:\Users\agilvarry\Documents\github\nand2tetris\10\ExpressionLessSquare'
    folders = [in_folder1, in_folder3, in_folder2]
    for in_folder in folders:
        out_folder = in_folder+'\output'
        for root, dirs, files in os.walk(in_folder):
            # select file name
            for file in files:
                # check the extension of files
                if file.endswith('.jack'):
                    file_name = file.split(".")[0] #this gets the name of the file minus .jack 
                    file_in = open(f"{in_folder}\\{file}", "r")
                    
                    tokenized_jack = Tokenizer.tokenize(file_in)
                    tokenizer_out = open(f"{out_folder}\\{file_name}T.xml", "w") #xml file to write
                    tokenizer_out.write(tokenized_jack)    
                    e = CompilationEngine(tokenized_jack)
                    compiled_jack= e.Engine()
                    compilation_out=open(f"{out_folder}\\{file_name}.xml", "w")
                    compilation_out.write(compiled_jack)
