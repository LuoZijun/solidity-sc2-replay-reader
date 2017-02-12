#!/usr/bin/env python
# coding: utf-8


# library for reading MPQ (MoPaQ) archives.

from __future__ import print_function

import platform
import os, struct, zlib, bz2
from struct import unpack, pack
from io import BytesIO

MPQ_FILE_IMPLODE        = 0x00000100
MPQ_FILE_COMPRESS       = 0x00000200
MPQ_FILE_ENCRYPTED      = 0x00010000
MPQ_FILE_FIX_KEY        = 0x00020000
MPQ_FILE_SINGLE_UNIT    = 0x01000000
MPQ_FILE_DELETE_MARKER  = 0x02000000
MPQ_FILE_SECTOR_CRC     = 0x04000000
MPQ_FILE_EXISTS         = 0x80000000

# <4s2I2H4I
MPQ_HEADER_KEYS = (
    'magic', 'header_size', 'archive_size', 'format_version', 
    'sector_size_shift', 'hash_table_offset', 'block_table_offset',
    'hash_table_entries', 'block_table_entries'
)

# q2h
MPQ_HEADER_EXT_KEYS = (
    'extended_block_table_offset', 'hash_table_offset_high', 
    'block_table_offset_high'
)

# '<4s3I'
MPQ_USER_DATA_HEADER_KEYS = (
    'magic', 'user_data_size', 'mpq_header_offset', 
    'user_data_header_size'
)

# '2I2HI'
MPQ_HASH_TABLE_ENTRY_KEYS = (
    'hash_a', 'hash_b', 'locale', 'platform', 'block_table_index'
)

# '4I'
MPQ_BLOCK_TABLE_ENTRY_KEYS = (
    'offset', 'archived_size', 'size', 'flags'
)

"""
C++ Data Type:

     8 bit = BYTE
    16 bit = WORD
    32 bit = DWORD
    64 bit = QWORD (quad-word).

C Data Type:


"""
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
        words = 4
        if platform.architecture()[0] == '64bit':
            words = 8
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
        words = 4
        if platform.architecture()[0] == '64bit':
            words = 8
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
        _bytes = self.read_byte(length=length/8)
        bits = []
        for n in _bytes:
            _bits = []
            while n != 0:
                m = n % base
                n = n / base
                _bits.append(m)
            for n in range(8-len(_bits)):
                _bits.append(0)
            # _bits.reverse()
            bits.extend(_bits)
        bits.reverse()
        while bits[0] == 0:
            bits = bits[1:]
        return bits

    def read_byte(self, length=1):
        return self.read_u8(length=length)
    def read_string(self, length):
        return str(self.file.read(length))

    def seek(self, pos):
        return self.file.seek(pos)

class Archive(object):
    file = None
    def __init__(self, file):
        assert(hasattr(file, 'read'))
        self.file = file
    
    def parse(self):
        self.parse_header()

    def parse_header(self):
        magic = self.file.read(4)
        self.file.seek(0)
        if magic == b'MPQ\x1a':
            header = read_mpq_header()
            header['offset'] = 0
        elif magic == b'MPQ\x1b':
            pass
        else:
            raise ValueError("Invalid file header.")

    def files(self):
        pass
    def tables(self):
        pass
    def header(self):
        pass


def open_file(filename):
    file = open(filename, 'rb')
    archive = Archive(file)
    archive.parse()
    return archive

def usage():
    msg = """
        $ python mpq.py target.mpq

    """
    print(usage)

import binascii

def test_buffer_reader():
    # Raw  <4s2I2H4I
    f  = open("test.replay", "rb")
    size = 4*1 + 2*4 + 2*2 + 4*4
    print(unpack("<4s2I2H4I", f.read(size)))

    # reader
    f2 = open("test.replay", "rb")
    buff = BufferReader(f2)
    res = (
        buff.read_u32(length=1),
        buff.read_u32(length=2),
        buff.read_u16(length=2),
        buff.read_u32(length=4),
    )
    print(res)

    # Bits
    f2 = open("test.replay", "rb")
    buff = BufferReader(f2)
    bits = buff.read_bit(length=8*4)
    bits = map(lambda n: str(n), bits)
    print("".join(bits))
    print("Num: 458313805  Bin: ", bin(458313805).replace("0b", ""))

    code = list("MPQ\x1b")
    _bytes = map(lambda s: ord(s), code)
    _result = map(lambda n: bin(n).replace("0b", ""), _bytes)
    print(_result)

def main(*args, **kwargs):
    # archive = open("test.replay")
    # print(archive)
    test_buffer_reader()

if __name__ == '__main__':
    main()
