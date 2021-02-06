import sys
import os

from compress import compress
from decompress import decompress

ENCODING = 'utf-8'
KEY_SIZE = 3
CHAR_SIZE = 2
MAX_INT_SIZE = 10

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    
    if operation == '-c':
        compress(input_file, output_file)
    elif operation == '-x':
        decompress(input_file, output_file)

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