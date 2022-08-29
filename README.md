# File-Compressor
 A file-compressor implementation based on Huffman Coding, a lossless data compression algorithm.
 
 It is a Python program that can be used to compress and decompress any text file. The idea is implemented using Huffman coding and heap data structure.
 
 While compressing, a minimum heap structure of characters appearing in the text file is created using the frequency of the characters as the
 comparing parameter. With of help of the heap, the Huffman tree is generated and variable-length codes are assigned to every node. The Huffman encoded input file is 
 saved.
 
 While decompressing, the encoded file is read and the Huffman tree is reconstructed. The characters are decoded by traversing the reconstructed tree and appeneded to
 the output file.
