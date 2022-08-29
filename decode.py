import huffman as hf
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Failed to detect files.")
        exit()
    
    f = hf.Huffman(sys.argv[1], sys.argv[2])
    f.decompress()
    print("Decompressed successfully")