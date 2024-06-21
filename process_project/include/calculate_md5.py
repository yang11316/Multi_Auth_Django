from cryptography.hazmat.primitives import hashes
import sys


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename , 'rb')as f:
        filehash = hashes.Hash(hashes.MD5())
        while chunk:=f.read(4096):
            filehash.update(chunk)
        print(filehash.finalize().hex())