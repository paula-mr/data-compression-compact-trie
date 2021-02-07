from constants import KEY_SIZE, CHAR_SIZE, MAX_INT_SIZE, ENCODING

def decompress(input_file, output_file):
    encoded_compressed_text = ''
    with open(input_file, 'rb') as file:
        byte = file.read(KEY_SIZE)
        while byte:
            key = int.from_bytes(byte, "big")
            encoded_compressed_text = encoded_compressed_text + str(key).zfill(MAX_INT_SIZE)
            byte = file.read(CHAR_SIZE)
            if byte:
                decoded = str(byte.decode(ENCODING)).replace('\x00','')
                encoded_compressed_text = encoded_compressed_text + decoded
                byte = file.read(KEY_SIZE)
    
    decompressed = __decompress_text(encoded_compressed_text)

    with open(output_file, 'w', encoding=ENCODING) as file:
        file.write(decompressed)
    

def __decompress_text(encoded_text):
    result = ''
    dictionary = {0: ''}
    index = 1
    block_size = MAX_INT_SIZE + 1

    for i in range(0, len(encoded_text), block_size):
        #concat computed result
        key = int(encoded_text[i:i+MAX_INT_SIZE])
        result = result + dictionary[key]

        #if there's a new char, add it to the dict and to the result
        if i+MAX_INT_SIZE < len(encoded_text):
            char = str(encoded_text[i+MAX_INT_SIZE:i+block_size])
            result = result + char
            dictionary[index] = dictionary[key] + char
            index = index + 1

    return result