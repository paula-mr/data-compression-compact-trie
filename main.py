import sys
import os

from compressed_trie import Trie

ENCODING = 'utf-8'
KEY_SIZE = 3
CHAR_SIZE = 2

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    
    if operation == '-c':
        compress(input_file, output_file)
    elif operation == '-x':
        decompress(input_file, output_file)

def compress(input_file, output_file):
    t = Trie(ENCODING, KEY_SIZE)
    with open(input_file, 'r') as file:
        t.create(file.read())
    
    compressed_result = t.output
    if output_file:
        file_name = output_file
    else:
        file_name = input_file.replace('.txt', '.z78')

    with open(file_name, 'wb') as file:
        file.write(compressed_result)

def decompress(input_file, output_file):
    encoded_compressed_text = ''
    with open(input_file, 'rb') as file:
        byte = file.read(KEY_SIZE)
        while byte:
            key = int.from_bytes(byte, "big")
            encoded_compressed_text = encoded_compressed_text + str(key).zfill(10)
            byte = file.read(CHAR_SIZE)
            if byte:
                decoded = byte.decode(ENCODING)
                encoded_compressed_text = encoded_compressed_text + decoded.zfill(CHAR_SIZE)
                byte = file.read(KEY_SIZE)
    
    decompressed = __decompress_text(encoded_compressed_text)
    
    if output_file:
        file_name = output_file
    else:
        file_name = input_file.replace('.z78', '.txt')

    with open(file_name, 'w', encoding=ENCODING) as file:
        file.write(decompressed)
    

def __decompress_text(encoded_text):
    result = ''
    dictionary = {0: ''}
    index = 1

    for i in range(0, len(encoded_text), 10 + CHAR_SIZE):
        #concat computed result
        key = int(encoded_text[i:i+10])
        result = result + dictionary[key]

        #if there's a new char, add it to the dict and to the result
        if i+10 < len(encoded_text):
            char = str(encoded_text[i+10:i+10+CHAR_SIZE])
            result = result + char
            dictionary[index] = dictionary[key] + char
            index = index + 1

    return result

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