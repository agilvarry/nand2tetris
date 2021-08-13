import Tokenizer
import os

if __name__ == "__main__":
     in_folder =r'C:\Users\agilvarry\Documents\github\nand2tetris\10\Square'
     out_folder = in_folder+'\output'
     for root, dirs, files in os.walk(in_folder):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.jack'):
                file_name = file.split(".")[0] #this gets the name of the file minus .jack 
                file_in = open(in_folder + "\\"+ file, "r")
                tokenized_jack = Tokenizer.tokenize(file_in)

                
                print(file_name)
                out = open(out_folder +"\\"+ file_name+'T'+".xml", "w")
                out.write(tokenized_jack)    