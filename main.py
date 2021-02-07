import sys
import os

from compress import compress
from decompress import decompress

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    
    if operation == '-c':
        if output_file:
            file_name = output_file
        else:
            file_name = input_file.replace('.txt', '.z78')
        compress(input_file, file_name)
    elif operation == '-x':
        if output_file:
            file_name = output_file
        else:
            file_name = input_file.replace('.z78', '.txt')
        decompress(input_file, file_name)

def get_startup_arguments(argv):
    operation = None
    input_file = None
    output_file = None

    if len(argv) >= 2:
        operation = argv[0]
        input_file = argv[1]
        if len(argv) == 4:
            output_file = argv[3]
    else:
        print('Invalid arguments')
        print("main.py <OPERATION> <INPUT FILE> [-o OUTPUT FILE]")
        os._exit(1)
    
    return operation, input_file, output_file

if __name__ == "__main__":
    main(sys.argv[1:])