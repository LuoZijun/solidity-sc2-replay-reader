#!/usr/bin/env python
# coding: utf-8

from __future__ import division
# import sys, os, time, platform, math
# from struct import unpack, pack

# Copy from https://golang.org/src/hash/adler32/adler32.go

# // mod is the largest prime that is less than 65536.
MOD  = 65521;
# // nmax is the largest n such that
# // 255 * n * (n+1) / 2 + (n+1) * (mod-1) <= 2^32-1.
# // It is mentioned in RFC 1950 (search for "5552").
NMAX = 5552;

def u32(n):
    # Min: 0, Max: 4294967295
    min_value = 0
    max_value = 4294967295
    if type(n) == float:
        n = int(n)
    if n < min_value:
        return 0
    elif n >= 0 and n <= max_value:
        return n
    elif n > max_value:
        return u32(n - max_value - 1)
    else:
        raise ValueError('Ooops(%d)...' % n)

def update(d, p):
    s1 = u32(d & 0xffff)
    s2 = u32(d >> 16)
    while len(p) > 0:
        q = []
        if len(p) > NMAX:
            p, q = p[:NMAX], p[NMAX:]
        while len(p) >= 4:
            s1 += u32(p[0])
            s2 += s1

            s1 += u32(p[1])
            s2 += s1

            s1 += u32(p[2])
            s2 += s1

            s1 += u32(p[3])
            s2 += s1

            p = p[4:]

        for x in p:
            s1 += u32(x)
            s2 += s1

        s1 %= MOD
        s2 %= MOD
        p = q
    return u32(s2 << 16 | s1)

def check_sum(data):
    digest = 1
    p = map(lambda s: ord(s), list(data))
    return update(digest, p)


def main():
    s = "hello, 世界！"
    digest = check_sum(s)
    hex_digest = hex(digest)
    # 1096681671 (0x415e08c7)
    print "D: %d  Hex: %s" % (digest, hex_digest) 

if __name__ == '__main__':
    main()