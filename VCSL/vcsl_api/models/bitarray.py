import gzip
import base64


class BitArray:
    def __init__(self, size=(2**17), id=None):
        self.array = '\x00' * (size // 8)
        # convert to ascii
        self.array = bytearray(self.array.encode('ascii'))  # Compressed bitarray is encoded in utf-8, but the bit array is in ascii
        self.size = size
        self.free = size
        self.id = id

    def __getitem__(self, index):
        return 1 if self.array[index // 8] & (1 << (index % 8)) != 0 else 0

    def __setitem__(self, index, value):
        if value not in [0, 1]:
            raise ValueError("BitArray only accepts 0 or 1")
        prev = self[index]
        if value == 1:
            self.array[index // 8] = self.array[index // 8] | (1 << (index % 8))
            if prev == 0:
                self.free -= 1
        else:
            self.array[index // 8] = self.array[index // 8] & ~(1 << (index % 8))
            if prev == 1:
                self.free += 1

    def __len__(self):
        return self.size

    def __str__(self):
        string = ''
        for i in range(self.size):
            string += '1' if self[i] else '0'
        return string

    def compress(self):
        gzip_compressed = gzip.compress(self.array)
        base64_compressed = base64.b64encode(gzip_compressed)
        return base64_compressed

    @classmethod
    def decompress(cls, compressed, size=(2**17), id=None):
        uncompressed_base64 = base64.b64decode(compressed)
        uncompressed = gzip.decompress(uncompressed_base64)
        bitarray = cls(size)
        bitarray.array = bytearray(uncompressed)
        bitarray.id = id
        for i in range(bitarray.size):  # TODO: Rethink another way to do this
            if bitarray[i]:
                bitarray.free -= 1
        return bitarray
