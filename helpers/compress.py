class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


def calculate_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

def build_huffman_tree(frequency):
    nodes = [Node(char, freq) for char, freq in frequency.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes[0]
        right = nodes[1]
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        nodes = nodes[2:] + [merged]
    return nodes[0] if nodes else None

def build_codes(node, prefix='', codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_encode(text):
    frequency = calculate_frequency(text)
    huffman_tree = build_huffman_tree(frequency)
    codes = build_codes(huffman_tree)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, codes

word = "hello world"
encoded_text, codes = huffman_encode(word)
print("Encoded text:", encoded_text)
print("Huffman Codes:", codes)
