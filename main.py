import sys
import os

from compressed_trie import Trie

def main(argv):
    operation, input_file, output_file = get_startup_arguments(argv)
    
    if operation == '-c':
        compress(input_file, output_file)
    elif operation == '-x':
        decompress(input_file, output_file)

def compress(input_file, output_file):
    t = Trie()
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
    encoded_decompressed_text = ''
    with open(input_file, 'rb') as file:
        byte = file.read(8)
        while byte:
            key = int.from_bytes(byte, "big")
            encoded_decompressed_text = encoded_decompressed_text + str(key).zfill(8)
            byte = file.read(8)
            if byte:
                decoded = byte.decode('utf-32')
                encoded_decompressed_text = encoded_decompressed_text + decoded
                byte = file.read(8)
    
    decompressed = __decompress_text(encoded_decompressed_text)
    
    if output_file:
        file_name = output_file
    else:
        file_name = input_file.replace('.z78', '.txt')

    with open(file_name, 'w') as file:
        file.write(decompressed)
    

def __decompress_text(encoded_text):
    result = ''
    dictionary = {0: ''}
    index = 1

    for i in range(0, len(encoded_text), 9):
        #concatenar resultado já computado
        a = int(encoded_text[i:i+8])
        result = result + dictionary[a]

        #se houver character compactado, adicioná-lo ao resultado e ao dictionary
        if i+8 < len(encoded_text):
            b = encoded_text[i+8]
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
        if len(argv) == 4:
            output_file = argv[3]
    else:
        print('Invalid arguments')
        print("main.py <OPERATION> <INPUT FILE> [-o OUTPUT FILE]")
        os._exit(1)
    
    return operation, input_file, output_file

if __name__ == "__main__":
    main(sys.argv[1:])