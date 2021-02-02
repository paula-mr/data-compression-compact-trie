import sys
import os

from compressed_trie import Trie

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    
    compressed = compress('ABAABABAABAB')
    decompressed = decompress(compressed)
    print(decompressed)

def compress(text):
    t = Trie()
    t.create(text)
    return t.output

def decompress(encoded_text):
    result = ''
    dictionary = {0: ''}
    index = 1

    for i in range(0, len(encoded_text), 2):
        a = int(encoded_text[i])
        result = result + dictionary[a]
        if i+1 < len(encoded_text):
            b = encoded_text[i+1]
            result = result + b
            dictionary[index] = dictionary[a] + b
            index = index + 1

    return result

def get_startup_arguments(argv):
    operation = None
    input_file = None
    output_file = None

    if len(argv) >= 2:
        operation = argv[0]
        input_file = argv[1]
        if len(argv) == 3:
            output_file = argv[2]
    else:
        print('Invalid arguments')
        print("main.py <OPERATION> <INPUT FILE> [OUTPUT FILE]")
        os._exit(1)
    
    return operation, input_file, output_file

if __name__ == "__main__":
    main(sys.argv[1:])