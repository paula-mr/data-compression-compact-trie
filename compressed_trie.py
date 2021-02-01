class Trie:
    index: 1
    children: {}
    output: []

    def __init__(self):
        self.index = 1
        self.root = {'': {'indexes':[0], 'children':{}}}
        self.output = ''

    def create(self, text):
        word = ""
        index = 1
        inserted = False
        father_node = None
        for c in text:
            aux = word + c
            father_node, inserted = self.insert(aux, index, self.root[''])
            if not inserted:
                word = aux
            else:
                word = ""
                index = index + 1
                self.output = self.output + str(father_node) + c
        if not inserted: #if last isn't inserted, only add the index to the output
            self.output = self.output + str(father_node)

    def insert(self, word, index, node):
        dictionary = node['children']
        for key in dictionary:
            if word == key: #if the word is already included, return index
                return dictionary[key]['indexes'][-1], False
            elif word.startswith(key):
                if dictionary[key]['children']: #if there are children, insert key as a child
                    return self.insert(word[len(key):len(word)], index, dictionary[key])
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
                        #create broken node
                        children = dictionary[key]['children']
                        indexes = dictionary[key]['indexes']
                        broken_node = {'indexes':indexes[i:len(key)], 'children':children}
                        dictionary.pop(key)
                        #get new values for father node
                        new_children = {word[i:len(word)]: {'indexes':[index], 'children':{}}, key[i:len(key)]: broken_node}
                        new_indexes = indexes[0:i]
                        dictionary[key[0:i]] = {'indexes':new_indexes, 'children':new_children}
                        return new_indexes[-1], True
                    i = i - 1
        #insert prefix if it doesn't exist
        dictionary[word] = {'indexes':[index], 'children':{}}
        return node['indexes'][-1], True
