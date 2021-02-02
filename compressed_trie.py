class Trie:
    index: 1
    children: {}
    output: []

    def __init__(self):
        self.index = 1
        self.root = {'': {'indexes':[0], 'children':{}}}
        self.output = bytearray(0)

    def create(self, text):
        word = ""
        index = 1
        inserted = False
        father_node = None
        for c in text:
            aux = word + c
            father_node, inserted = self.__insert(aux, index, self.root[''])
            if not inserted:
                word = aux #continue processing until a new segment is inserted
            else:
                word = ""
                index = index + 1
                self.__format_output(father_node, c)
        if not inserted: #if last isn't inserted, only add the index to the output
            self.__format_output(father_node)

    def __insert(self, word, index, node):
        dictionary = node['children']
        for key in dictionary:
            if word == key: #if the word is already included, return index
                return dictionary[key]['indexes'][-1], False
            elif word.startswith(key):
                if dictionary[key]['children']: #if there are children, insert key as a child
                    return self.__insert(word[len(key):len(word)], index, dictionary[key])
                else: #if there aren't children, compact node
                    indexes = dictionary[key]['indexes']
                    last_index = indexes[-1]
                    indexes.append(index)
                    dictionary.pop(key)
                    dictionary[word] = {'indexes':indexes, 'children':{}}
                    return last_index, True
            else: #check if should break any nodes
                i = len(key) - 1
                while i > 0:
                    if word == key[0:i]: #if word is included in a key, return corresponding index
                        new_indexes = dictionary[key]['indexes'][0:i]
                        return new_indexes[-1], False
                    if word.startswith(key[0:i]): #if the word starts with a partial key, break the node
                        #remove original node
                        children = dictionary[key]['children']
                        indexes = dictionary[key]['indexes']
                        dictionary.pop(key)
                        
                        #create node for original sufix
                        original_sufix = key[i:len(key)]
                        original_sufix_indexes = indexes[i:len(key)]
                        original_sufix_node = self.__create_node(original_sufix_indexes, children)

                        #create node for new sufix
                        new_sufix = word[i:len(word)]
                        new_sufix_node = self.__create_node([index], {})

                        #create new prefix node
                        prefix = key[0:i]
                        prefix_indexes = indexes[0:i]
                        new_children = {new_sufix: new_sufix_node, original_sufix: original_sufix_node}
                        dictionary[prefix] = self.__create_node(prefix_indexes, new_children)

                        #return prefix index
                        return prefix_indexes[-1], True
                    # decrement i
                    i = i - 1

        #insert prefix if it doesn't exist
        dictionary[word] = {'indexes':[index], 'children':{}}
        return node['indexes'][-1], True

    def __create_node(self, indexes, children):
        return {'indexes': indexes, 'children': children}

    def __format_output(self, number, c = ''):
        encoded_number = number.to_bytes(length=8, byteorder='big')
        encoded_char = c.encode('utf-32')
        self.output = b''.join([self.output, encoded_number, encoded_char])
