#!/usr/bin/env python
# coding: utf-8

from __future__ import division
# import sys, os, time, platform, math
# from struct import unpack, pack

# Copy from https://golang.org/src/hash/adler32/adler32.go

# // BASE is the largest prime that is less than 65536.
BASE = 65521;
# // nmax is the largest n such that
# // 255 * n * (n+1) / 2 + (n+1) * (BASE-1) <= 2^32-1.
# // It is mentioned in RFC 1950 (search for "5552").
NMAX = 5552;

U32_MAX_VALUE = 4294967295
U32_MIN_VALUE = 0

def u32(n):
    if type(n) == float: n = int(n)
    return min(max(n, U32_MIN_VALUE), U32_MAX_VALUE)

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

        s1 %= BASE
        s2 %= BASE
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