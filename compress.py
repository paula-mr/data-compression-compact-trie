import os
from constants import ENCODING, KEY_SIZE, CHAR_SIZE

def compress(input_file, output_file):
    t = Trie()
    with open(input_file, 'r') as file:
        t.create(file.read())
    
    compressed_result = t.output

    with open(output_file, 'wb') as file:
        file.write(compressed_result)

class Trie:
    def __init__(self):
        self.index = 1
        self.root = {'': {'indexes':[0], 'children':{}}}
        self.output = bytearray(0)

    def create(self, text):
        word = ""
        inserted = False
        father_node = None
        for c in text:
            aux = word + c
            father_node, inserted = self.__insert(aux, self.index, self.root[''])
            if not inserted:
                word = aux #continue processing until a new segment is inserted
            else: #add tuple to output
                word = ""
                self.index = self.index + 1
                self.__format_output(father_node, c)
        if not inserted: #if last isn't inserted, only add the index to the output
            self.__format_output(father_node)

    def __insert(self, word, index, node):
        dictionary = node['children']
        if dictionary.get(word): #if the word is already included, return index
            return dictionary[word]['indexes'][-1], False
        for key in dictionary:
            if word.startswith(key):
                if dictionary[key]['children']: #if there are children, insert key as a child
                    return self.__insert(word[len(key):len(word)], index, dictionary[key])
                else: #if there aren't children, compact node
                    father_node = self.__compact_node(dictionary, key, index, word)
                    return father_node, True
            else: #check if should break any nodes
                i = len(key) - 1
                while i > 0:
                    if word == key[0:i]: #if word is included in a key, return corresponding index
                        return dictionary[key]['indexes'][i], False
                    if word.startswith(key[0:i]): #if the word starts with a partial key, break the node
                        father_node = self.__break_node(dictionary, key, i, word)
                        return father_node, True
                    i = i - 1

        #insert prefix if it doesn't exist
        dictionary[word] = {'indexes':[index], 'children':{}}
        return node['indexes'][-1], True

    def __compact_node(self, dictionary, key, index, word):
        indexes = dictionary[key]['indexes']
        father_node = indexes[-1] #save father node
        indexes.append(index)
        dictionary.pop(key)
        dictionary[word] = {'indexes':indexes, 'children':{}}
        return father_node

    def __break_node(self, dictionary, key, breaking_index, word):
        #remove original node
        children = dictionary[key]['children']
        indexes = dictionary[key]['indexes']
        dictionary.pop(key)
        
        #create node for original sufix
        original_sufix = key[breaking_index:len(key)]
        original_sufix_indexes = indexes[breaking_index:len(key)]
        original_sufix_node = self.__create_node(original_sufix_indexes, children)

        #create node for new sufix
        new_sufix = word[breaking_index:len(word)]
        new_sufix_node = self.__create_node([breaking_index], {})

        #create new prefix node
        prefix = key[0:breaking_index]
        prefix_indexes = indexes[0:breaking_index]
        new_children = {new_sufix: new_sufix_node, original_sufix: original_sufix_node}
        dictionary[prefix] = self.__create_node(prefix_indexes, new_children)

        #return father node
        return prefix_indexes[-1]

    def __create_node(self, indexes, children):
        return {'indexes': indexes, 'children': children}

    def __format_output(self, number, c = ''):
        encoded_number = number.to_bytes(length=KEY_SIZE, byteorder='big')
        encoded_char = self.__encode_char(c)
        self.output = b''.join([self.output, encoded_number, encoded_char])

    def __encode_char(self, char):
        encoded_char = char.encode(ENCODING)
        #if encoded char is smaller than char size, add padding
        if encoded_char and len(encoded_char) < CHAR_SIZE:
            encoded_char = b''.join([bytearray(CHAR_SIZE - len(encoded_char)), encoded_char])
        #if encoded char is bigger than char size, return error
        elif encoded_char and len(encoded_char) > CHAR_SIZE:
            print("Encoding ", char, " not supported")
            os._exit(1)
        return encoded_char
