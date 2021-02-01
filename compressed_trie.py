class Trie:
    index: 1
    children: {}
    output: []

    def __init__(self):
        self.index = 1
        self.children = {'': {'indexes':[0], 'children':{}}}
        self.output = []

    def create(self, text):
        word = ""
        index = 1
        for c in text:
            aux = word + c
            father_node, inserted = self.insert(aux, index, self.children[''])
            if not inserted:
                word = aux
            else:
                word = ""
                index = index + 1

    def insert(self, word, index, node):
        dictionary = node['children']
        for key in dictionary:
            if word == key:
                return None, False
            elif word.startswith(key):
                if dictionary[key]['children']: #if there are children then insert as a child
                    return self.insert(word[len(key):len(word)], index, dictionary[key])
                else: #if there aren't children compact node
                    indexes = dictionary[key]['indexes']
                    last_index = indexes[-1]
                    indexes.append(index)
                    dictionary.pop(key)
                    dictionary[word] = {'indexes':indexes, 'children':{}}
                    return last_index, True
            else: #check if should break any nodes
                i = len(key) - 1
                while i > 0:
                    if word == key[0:i]:
                        return i, False
                    if word.startswith(key[0:i]):
                        children = dictionary[key]['children']
                        indexes = dictionary[key]['indexes']
                        broken_node = {'indexes':indexes[i:len(key)], 'children':children}
                        dictionary.pop(key)

                        new_children = {word[i:len(word)]: {'indexes':[index], 'children':{}}, key[i:len(key)]: broken_node}
                        dictionary[key[0:i]] = {'indexes':indexes[0:i], 'children':new_children}
                        return i, True
                    i = i - 1

        dictionary[word] = {'indexes':[index], 'children':{}}
        return node['indexes'][-1], True
