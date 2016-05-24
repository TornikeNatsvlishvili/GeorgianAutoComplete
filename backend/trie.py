class Node:
    """Node for Python Trie Implementation"""

    def __init__(self):
        self.word = None
        self.extra_data = None
        self.nodes = {}  # dict of nodes

    def __get_all__(self):
        """Get all of the words in the trie"""
        x = []

        for key, node in self.nodes.items():
            if node.word is not None:
                x.append(node.word)

            x += node.__get_all__()

        return x

    def __get_all_data__(self):
        """Get all of the words in the trie"""
        x = []

        for key, node in self.nodes.items():
            if node.word is not None:
                x.append((node.word, node.extra_data))

            x += node.__get_all_data__()

        return x

    def __str__(self):
        return self.word

    def __insert__(self, word, string_pos=0, extra_data=None):
        """Add a word to the node in a Trie"""
        current_letter = word[string_pos]

        # Create the Node if it does not already exist
        if current_letter not in self.nodes:
            self.nodes[current_letter] = Node()

        if (string_pos + 1 == len(word)):
            self.nodes[current_letter].word = word
            self.nodes[current_letter].extra_data = extra_data
        else:
            self.nodes[current_letter].__insert__(word, string_pos + 1, extra_data)

        return True

    def __get_all_with_prefix__(self, prefix, string_pos):
        """Return all nodes in a trie with a given prefix or that are equal to the prefix"""
        x = []
        # if we satisfied prefix return all current node children
        if string_pos >= len(prefix):
            x += self.__get_all__()
        # else go onto next letter
        elif prefix[string_pos] in self.nodes:
            x += self.nodes[prefix[string_pos]].__get_all_with_prefix__(prefix, string_pos + 1)

        return x

    def __get_all_data_with_prefix__(self, prefix, string_pos):
        x = []
        # if we satisfied prefix return all current node children
        if string_pos >= len(prefix):
            x += self.__get_all_data__()
        # else go onto next letter
        elif prefix[string_pos] in self.nodes:
            x += self.nodes[prefix[string_pos]].__get_all_data_with_prefix__(prefix, string_pos + 1)

        return x

class Trie:
    """Trie Python Implementation"""

    def __init__(self):
        self.root = Node()

    def insert(self, word, data=None):
        self.root.__insert__(word, extra_data=data)

    def get_all(self):
        return self.root.__get_all__()

    def get_all_with_prefix(self, prefix, string_pos=0):
        return self.root.__get_all_with_prefix__(prefix, string_pos)

    def get_all_data_with_prefix(self, prefix, string_pos=0):
        return self.root.__get_all_data_with_prefix__(prefix, string_pos)


def load_kb(name):
    trie = Trie()
    with open('kb/{}'.format(name), 'r') as f:
        current_gram = ''
        for line in f:
            if not line.startswith('\t'):
                # context
                current_gram = line.strip()
            else:
                word, count = line.strip().split(':')
                trie.insert(word, int(count))

    return trie


if __name__ == '__main__':
    print("initializing word store...")
    trie = load_kb("0.txt")
    print("done")
    print(sorted(trie.get_all_data_with_prefix('გამარჯო'), key = lambda word: word[1], reverse=True))
