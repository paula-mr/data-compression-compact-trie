import sys
import os

from compressed_trie import Trie

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    t = Trie()
    t.create('ABAABABAABA')
    print(t.children)
    print(t.output)

def compress(text):
    index = 0
    dictionary = {'': {'index': [index], 'children': {}}}
    encoded_text = []

def insert(character, index, dictionary):
    for key in dictionary:
        pass

def lookup(word, dictionary):
    for key in dictionary:
        if word == key:
            return dictionary[key]
        if word.startswith(key):
            return lookup(word, dictionary[key][1])
    return None

def decompress(encoded_text):
    pass

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