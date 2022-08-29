import heapq

#Defining Huffman Tree Node
class Node:
    def __init__(self, data = None, freq = None, code = None, left = None, right = None):
        self.data = data
        self.freq = freq
        self.code = code
        self.left = left
        self.right = right

    #Overriding the comparison operator
    def __lt__(self, nxt):
        return self.freq < nxt.freq


class Huffman:
    arr = []
    root = None
    minHeap = []

    #Constructor
    def __init__(self, inFileName, outFileName):
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.create_arr()

    #Initializing a list of tree nodes representing character's ASCII value and initialize it's frequency with 0
    def create_arr(self):
        for i in range(128):
            self.arr.append(Node(i,0))

    #Traversing the constructed tree to generate huffman codes of each present character
    def traverse(self, root, str):
        if not root.left and not root.right:
            root.code = str
            return

        self.traverse(root.left, str + '0')
        self.traverse(root.right, str + '1')

    #Function to convert binary string to its equivalent decimal value
    def bin_to_dec(self, inStr):
        return int(inStr, 2)
    
    def dec_to_bin(self, inNum):
        return bin(inNum).replace('0b', '')

    def build_tree(self, aCode, path):
        cur = self.root
        for i in range(len(path)):
            if path[i] == '0':
                if cur.left is None:
                    cur.left = Node()
                cur = cur.left
            elif path[i] == '1':
                if cur.right is None:
                    cur.right = Node()
                cur = cur.right
        cur.data = aCode

    #Creating Min Heap of Nodes by frequency of characters in the input file
    def create_minHeap(self):
        with open(self.inFileName, mode = 'r', encoding = 'utf-8') as inFile:
            while 1:
                # Reading by character in the input file, incrementing frequency of each
                char = inFile.read(1)
                if not char:
                    break
                self.arr[ord(char)].freq += 1

        #Pushing the nodes which appear in the file into the priority queue
        for i in range(128):
            if self.arr[i].freq > 0:
                heapq.heappush(self.minHeap, self.arr[i])

    #Constructing the Huffman tree
    def create_tree(self):
        #Creating Huffman Tree with the Min Heap created earlier
        tempHeap = [node for node in self.minHeap]
        while len(tempHeap) != 1:
            left = heapq.heappop(tempHeap)
            right = heapq.heappop(tempHeap)

            self.root = Node()
            self.root.freq = left.freq + right.freq

            self.root.left = left
            self.root.right = right
            heapq.heappush(tempHeap, self.root)

    #Generating Huffman codes
    def create_codes(self):
        #Traversing the Huffman Tree and assigning specific codes to each character
        self.traverse(self.root, "")

    #Saving Huffman Encoded File
    def save_encodedFile(self):
        #Saving encoded (.huf) file
        inn = ""

        #Saving the meta data (Huffman tree)
        inn += chr(len(self.minHeap))
        tempHeap = [node for node in self.minHeap]
        while len(tempHeap) > 0:
            curr = tempHeap[0]
            inn += chr(curr.data)
            #Saving 16 decimal values representing code of curr.data
            s = ''.join(['0'] * (127 - len(curr.code)))
            s += '1'
            s += curr.code
            #Saving decimal values of every 8-bit binary code
            inn += chr(self.bin_to_dec(s[0:8]))
            for i in range(15):
                s = s[8:]
                inn += chr(self.bin_to_dec(s[0:8]))
            heapq.heappop(tempHeap)
        s = ""

        #Saving codes of every character appearing in the input file
        with open(self.inFileName, mode = 'r', encoding = 'utf-8') as inFile:
            while 1:
                char = inFile.read(1)
                if not char:
                    break
                s += self.arr[ord(char)].code
                #Saving decimal values of every 8-bit binary code
                while len(s) > 8:
                    inn += chr(self.bin_to_dec(s[0:8]))
                    s = s[8:]

        #Finally if bits remaining are less than 8, append 0s
        count = 8 - len(s)
        if len(s) < 8:
            s += ''.join(['0'] * count)
        
        inn += chr(self.bin_to_dec(s))
        #Append count of appended 0s
        inn += chr(count)

        #Write the inn string to the output file
        byteString = inn.encode('utf-8')
        with open(self.outFileName, mode = 'wb') as outFile:
            outFile.write(byteString)

    def save_decodedFile(self):
        with open(self.inFileName, mode = 'rb') as inFile:
            size = int.from_bytes(inFile.read(1), 'big')
            #Reading count at the end of the file which is number of bits appended to make final value 8-bit
            inFile.seek(-1, 2)                  #2 is used to set the reference point from the end of the file
            count0 = int.from_bytes(inFile.read(1),'big')
            #Ignoring the meta data (huffman tree) (1 + 17 * size) and reading remaining file
            inFile.seek(1 + 17 * size, 0)       #0 is used to set the reference point from the start of the file

            text = []
            while 1:
                textseg = int.from_bytes(inFile.read(1), 'big')
                if not textseg:
                    break
                text.append(textseg)

        with open(self.outFileName, mode = 'a', encoding = 'utf-8') as outFile:
            cur = self.root
            for i in range(len(text) - 1):
                #Converting decimal number to its equivalent 8-bit binary code
                path = self.dec_to_bin(text[i])
                if i == len(text) - 2:
                    path = path[0: 8 - count0]
                #Traversing huffman tree and appending resultant data to the file
                for j in range(len(path)):
                    if path[j] == '0':
                        cur = cur.left
                    else:
                        cur = cur.right
                    
                    if cur.left is None and cur.right is None:
                        s = cur.data.decode('utf-8')
                        outFile.write(s)
                        cur = self.root

    def get_tree(self):
        with open(self.inFileName, mode = 'rb') as inFile:
            #Reading size of minHeap
            size = int.from_bytes(inFile.read(1), 'big')
            self.root = Node()
            #Next size * (1 + 16) characters contain (char)data and (string)code[in decimal]
            for i in range(size):
                aCode = inFile.read(1)
                hCodeC = []
                for j in range(16):
                    hCodeC.append(int.from_bytes(inFile.read(1), 'big'))
                #Converting decimal characters into their binary equivalent to obtain code
                hCodeStr = ""
                for j in range(16):
                    hCodeStr += self.dec_to_bin(hCodeC[j])
                #Removing padding by ignoring first (127 - len(curr.code)) 0s and next 1 character
                j = 0
                while hCodeStr[j] == '0':
                    j += 1
                hCodeStr = hCodeStr[j + 1:]
                #Adding node with aCode data and hCodeStr string to the huffman tree
                self.build_tree(aCode, hCodeStr)


    def compress(self):
        self.create_minHeap()
        self.create_tree()
        self.create_codes()
        self.save_encodedFile()

    def decompress(self):
        self.get_tree()
        self.save_decodedFile()