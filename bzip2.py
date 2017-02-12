#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import sys, os, time, platform, math
from struct import unpack, pack

class BufferReader(object):
    def __init__(self, file, endian="<"):
        assert(hasattr(file, 'read'))
        self.file = file
        self.endian = endian
    def read_u8(self, length=1):
        # unsigned char 
        return unpack(self.endian + "%dB" % length, self.file.read(1*length))
    def read_u16(self, length=1):
        # unsigned short
        return unpack(self.endian + "%dH" % length, self.file.read(2*length))
    def read_u32(self, length=1):
        # unsigned int
        return unpack(self.endian + "%dI" % length, self.file.read(4*length))
    def read_usize(self, length=1):
        # unsigned long
        if platform.architecture()[0] == '64bit':
            words = 8
        elif platform.architecture()[0] == '32bit':
            words = 4
        elif platform.architecture()[0] == '16bit':
            words = 2
        else:
            raise ValueError('Ooops...')

        return unpack(self.endian + "%dL" % length, self.file.read(words*length))
    def read_u64(self, length=1):
        # unsigned long long
        return unpack(self.endian + "%dQ" % length, self.file.read(8*length))

    def read_i8(self, length=1):
        # signed char
        return unpack(self.endian + "%db" % length, self.file.read(1*length))
    def read_i16(self, length=1):
        # short
        return unpack(self.endian + "%dh" % length, self.file.read(2*length))
    def read_i32(self, length=1):
        # int
        return unpack(self.endian + "%di" % length, self.file.read(4*length))
    def read_isize(self, length=1):
        # long
        if platform.architecture()[0] == '64bit':
            words = 8
        elif platform.architecture()[0] == '32bit':
            words = 4
        elif platform.architecture()[0] == '16bit':
            words = 2
        else:
            raise ValueError('Ooops...')
        return unpack(self.endian + "%dl" % length, self.file.read(words*length))
    def read_i64(self, length=1):
        # long long
        return unpack(self.endian + "%dq" % length, self.file.read(8*length))

    def read_f32(self, length=1):
        # float
        return unpack(self.endian + "%df" % length, self.file.read(4*length))
    def read_f64(self, length=1):
        # double
        return unpack(self.endian + "%dd" % length, self.file.read(8*length))

    def read_bit(self, length=8):
        assert(length%8 == 0)
        base   = 2
        _bytes = self.read_byte(length=length//8)
        bits = []
        for n in _bytes:
            _bits = []
            while n != 0:
                m = n % base
                n = n // base
                _bits.append(m)
            for n in range(8-len(_bits)):
                _bits.append(0)
            if self.endian == '>' or self.endian == '!':
                _bits.reverse()
            bits.extend(_bits)
        if self.endian == '<':
            bits.reverse()
        # while bits[0] == 0:
        #   bits = bits[1:]
        return tuple(bits)

    def read_byte(self, length=1):
        return self.read_u8(length=length)
    def read_string(self, length):
        return str(self.file.read(length))

    def seek(self, pos):
        return self.file.seek(pos)


class HuffmanLength:
    def __init__(self, code, bits = 0):
        self.code = code
        self.bits = bits
        self.symbol = None
    def __repr__(self):
        return `(self.code, self.bits, self.symbol, self.reverse_symbol)`
    def __cmp__(self, other):
        if self.bits == other.bits:
            return cmp(self.code, other.code)
        else:
            return cmp(self.bits, other.bits)

def reverse_bits(v, n):
    a = 1 << 0
    b = 1 << (n - 1)
    z = 0
    for i in range(n-1, -1, -2):
        z |= (v >> i) & a
        z |= (v << i) & b
        a <<= 1
        b >>= 1
    return z

def reverse_bytes(v, n):
    a = 0xff << 0
    b = 0xff << (n - 8)
    z = 0
    for i in range(n-8, -8, -16):
        z |= (v >> i) & a
        z |= (v << i) & b
        a <<= 8
        b >>= 8
    return z

class HuffmanTable:
    def __init__(self, bootstrap):
        l = []
        start, bits = bootstrap[0]
        for finish, endbits in bootstrap[1:]:
            if bits:
                for code in range(start, finish):
                    l.append(HuffmanLength(code, bits))
            start, bits = finish, endbits
            if endbits == -1:
                break
        l.sort()
        self.table = l

    def populate_huffman_symbols(self):
        bits, symbol = -1, -1
        for x in self.table:
            symbol += 1
            if x.bits != bits:
                symbol <<= (x.bits - bits)
                bits = x.bits
            x.symbol = symbol
            x.reverse_symbol = reverse_bits(symbol, bits)
            #print printbits(x.symbol, bits), printbits(x.reverse_symbol, bits)

    def tables_by_bits(self):
        d = {}
        for x in self.table:
            try:
                d[x.bits].append(x)
            except:
                d[x.bits] = [x]
        pass

    def min_max_bits(self):
        self.min_bits, self.max_bits = 16, -1
        for x in self.table:
            if x.bits < self.min_bits: self.min_bits = x.bits
            if x.bits > self.max_bits: self.max_bits = x.bits

    def _find_symbol(self, bits, symbol, table):
        for h in table:
            if h.bits == bits and h.reverse_symbol == symbol:
                #print "found, processing", h.code
                return h.code
        return -1

    def find_next_symbol(self, field, reversed = True):
        cached_length = -1
        cached = None
        for x in self.table:
            if cached_length != x.bits:
                cached = field.snoopbits(x.bits)
                cached_length = x.bits
            if (reversed and x.reverse_symbol == cached) or (not reversed and x.symbol == cached):
                field.readbits(x.bits)
                print "found symbol", hex(cached), "of len", cached_length, "mapping to", hex(x.code)
                return x.code
        raise "unfound symbol, even after end of table @ " + `field.tell()`
            
        for bits in range(self.min_bits, self.max_bits + 1):
            #print printbits(field.snoopbits(bits),bits)
            r = self._find_symbol(bits, field.snoopbits(bits), self.table)
            if 0 <= r:
                field.readbits(bits)
                return r
            elif bits == self.max_bits:
                raise "unfound symbol, even after max_bits"

class OrderedHuffmanTable(HuffmanTable):
    def __init__(self, lengths):
        l = len(lengths)
        z = map(None, range(l), lengths) + [(l, -1)]
        print "lengths to spans:", z
        HuffmanTable.__init__(self, z)

def code_length_orders(i):
    return (16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15)[i]

def distance_base(i):
    return (1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577)[i]

def length_base(i):
    return (3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258)[i-257]

def extra_distance_bits(n):
    if 0 <= n <= 1:
        return 0
    elif 2 <= n <= 29:
        return (n >> 1) - 1
    else:
        raise "illegal distance code"

def extra_length_bits(n):
    if 257 <= n <= 260 or n == 285:
        return 0
    elif 261 <= n <= 284:
        return ((n-257) >> 2) - 1
    else:
        raise "illegal length code"

def move_to_front(l, c):
    l[:] = l[c:c+1] + l[0:c] + l[c+1:]

def bwt_transform(L):
    # Semi-inefficient way to get the character counts
    F = ''.join(sorted(L))
    base = map(F.find,map(chr,range(256)))

    pointers = [-1] * len(L)
    for symbol, i in map(None, map(ord,L), xrange(len(L))):
        pointers[base[symbol]] = i
        base[symbol] += 1
    return pointers

def bwt_reverse(L, end):
    out = ''
    if len(L):
        T = bwt_transform(L)
        for i in xrange(len(L)):
            end = T[end]
            out += L[end]

    return out


def parse_header(buf):
    # 4 Byte
    assert(isinstance(buf, BufferReader))

    # 'BZ' signature/magic number
    # magic = buf.read_bit(length=16)
    magic = buf.read_string(length=2)
    assert(magic == 'BZ')

    # 'h' for Bzip2 ('H'uffman coding), '0' for Bzip1 (deprecated)
    version, = buf.read_string(length=1)
    assert(version == 'h')

    # '1'..'9' block-size 100 kB-900 kB (uncompressed)
    hundred_k_blocksize = buf.read_string(length=1)
    assert(hundred_k_blocksize in '123456789')

# const bzip2FileMagic  = 0x425a          # "BZ"
# const bzip2BlockMagic = 0x314159265359  # (49,  65, 89, 38, 83,  89)
# const bzip2FinalMagic = 0x177245385090  # (23, 114, 69, 56, 80, 144)

def bits_to_number(bits):
    return int("".join(map(lambda n: str(n), bits )), 2)

def parse_compressed_block(out, buf):
    assert(isinstance(buf, BufferReader))

    Huffman_Block_Magic       = (49,  65, 89, 38, 83,  89)  # 0x314159265359 BCD  (pi)
    End_of_Stream_Block_Magic = (23, 114, 69, 56, 80, 144)  # 0x177245385090 sqrt (pi)

    compressed_magic = buf.read_byte(length=6)
    crc = buf.read_byte(length=4)

    bits = []
    pos  = 0
    def need_bits(num):
        end = pos + num
        if end > len(bits):
            _bits = buf.read_bit(length=int(math.ceil((num - (len(bits) - pos))/8))*8)
            bits.extend(_bits)
        return bits[pos:end]

    if compressed_magic == End_of_Stream_Block_Magic:
        return out
    elif compressed_magic == Huffman_Block_Magic:
        # 'bzip2 Huffman block'
        # 1 + 24 + 0..256 + 3 + 15 + 1..6 + 5 + 1..40
        # 0=>normal, 1=>randomised (deprecated)
        randomised = need_bits(1)[0]
        pos += 1
        # print bits
        assert(randomised == 0)

        # starting pointer into BWT for after untransform
        orig_ptr = need_bits(24) # pointer
        pos += 24

        # bitmap, of ranges of 16 bytes, present/not present

        huffman_used_map = bits_to_number(need_bits(16)) # 0x8800
        pos += 16
        # if huffman_used_map:
        #     reduce(lambda a,b: a*2, range(15), 1)
        map_mask = 1 << 15 # 32768
        used = []  # huffman_used_bitmaps = 

        while map_mask > 0:
            if huffman_used_map & map_mask:
                # 16 bits
                huffman_used_bitmap = bits_to_number(need_bits(16))
                pos += 16

                bit_mask = 1 << 15
                while bit_mask > 0:
                    if huffman_used_bitmap & bit_mask:
                        pass
                    used += [bool(huffman_used_bitmap & bit_mask)]
                    bit_mask >>= 1
            else:
                used += [False] * 16
            map_mask >>= 1
        # print used
        huffman_groups = bits_to_number(need_bits(3))
        pos += 3

        print 'huffman groups', huffman_groups

        if not 2 <= huffman_groups <= 6:
            raise "Bzip2: Number of Huffman groups not in range 2..6"
        selectors_used = bits_to_number(need_bits(15))
        pos += 15
        mtf = range(huffman_groups)
        selectors_list = []

        for i in range(selectors_used):
            # zero-terminated bit runs (0..62) of MTF'ed huffman table 
            c = 0
            _tmp = bits_to_number(need_bits(1))
            pos += 1
            while _tmp:
                c += 1
                if c >= huffman_groups:
                    raise "Bzip2 chosen selector greater than number of groups (max 6)"
            if c >= 0:
                move_to_front(mtf, c)
            print c, mtf
            selectors_list += mtf[0:1]

        groups_lengths = []
        symbols_in_use = sum(used) + 2  # remember RUN[AB] RLE symbols
        for j in range(huffman_groups):
            length = start_huffman_length = bits_to_number(need_bits(5))
            pos += 5
            print 'start_huffman_length', start_huffman_length
            lengths = []
            for i in range(symbols_in_use):
                if not 0 <= length <= 20:
                    raise "Bzip2 Huffman length code outside range 0..20"
                _tmp = bits_to_number(need_bits(1))
                pos += 1
                while _tmp:
                    _tmp2 = bits_to_number(need_bits(1))
                    pos += 1
                    length -= (_tmp2 * 2) - 1
                    _tmp = bits_to_number(need_bits(1))
                    pos += 1
                lengths += [length]
            groups_lengths += [lengths]
            #print groups_lengths
        

        tables = []
        for g in groups_lengths:
            codes = OrderedHuffmanTable(g)
            codes.populate_huffman_symbols()
            codes.min_max_bits()
            tables.append(codes)

        #favourites = map(chr,range(sum(used)))
        #favourites = string.join([y for x,y in map(None,used,map(chr,range(len(used)))) if x],'')
        favourites = [y for x,y in map(None,used,map(chr,range(len(used)))) if x]

        selector_pointer = 0
        decoded = 0
        # Main Huffman loop
        repeat = repeat_power = 0
        buffer = ''
        t = None
        while True:
            decoded -= 1
            if decoded <= 0:
                decoded = 50 # Huffman table re-evaluate/switch length
                if selector_pointer <= len(selectors_list):
                    t = tables[selectors_list[selector_pointer]]
                    selector_pointer += 1
            print "Find Next Symbol: "

            reversed = False
            # r = find_next_symbol(t, False)
            # find_next_symbol start
            cached_length = -1
            cached = None
            stop = False
            r = None
            for x in t.table:
                if not stop:
                    if cached_length != x.bits:
                        # snoopbits
                        # cached = field.snoopbits(x.bits)
                        cached = bits_to_number(need_bits(x.bits))
                        pos += x.bits
                        cached_length = x.bits
                    if (reversed and x.reverse_symbol == cached) or (not reversed and x.symbol == cached):
                        # field.readbits(x.bits)
                        bits_to_number(need_bits(x.bits))
                        pos += x.bits
                        print "found symbol", hex(cached), "of len", cached_length, "mapping to", hex(x.code)
                        r = x.code
                        stop = True
            if not stop:
                raise Exception("unfound symbol, even after end of table @%d " % pos)
            # find_next_symbol end

            if 0 <= r <= 1:
                if repeat == 0:
                    repeat_power = 1
                repeat += repeat_power << r
                repeat_power <<= 1
                continue
            elif repeat > 0:
                buffer += favourites[0] * repeat
                repeat = 0
            if r == symbols_in_use - 1:
                break
            else:
                o = favourites[r-1]
                move_to_front(favourites, r-1)
                buffer += o
                pass

        nt = nearly_there = bwt_reverse(buffer, pointer)
        done = ''
        i = 0
        while i < len(nearly_there):
            if i < len(nearly_there) - 4 and nt[i] == nt[i+1] == nt[i+2] == nt[i+3]:
                done += nearly_there[i] * (ord(nearly_there[i+4]) + 4)
                i += 5
            else:
                done += nearly_there[i]
                i += 1
        out += done
        print "Pos: ", pos, " Bits Length: ", len(bits)
        sys.exit(1)
    else:
        raise "Illegal Bzip2 blocktype"


def bzip2_main(buf):
    # https://en.wikipedia.org/wiki/Bzip2#File_format
    parse_header(buf)

    out = parse_compressed_block('', buf)


def decompress(data):
    pass


def main():
    filename = "pyflate/testdata/aaa.bz2"
    file = open(filename, "rb")
    buf = BufferReader(file, endian=">")
    out = bzip2_main(buf)
    print("Data: %s" % out)

if __name__ == '__main__':
    main()