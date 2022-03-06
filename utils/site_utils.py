import re
from urllib.parse import quote, unquote
from ctypes import c_int32 as i32

# ================================================================

def tear_decode(data_file, data_seed):
    def replacer(match):
        chars = {
            '0': '5',
            '1': '6',
            '2': '7',
            '5': '0',
            '6': '1',
            '7': '2'
        }
        return chars[match.group(0)]

    def str2bytes(a16):
        a21 = []
        for i in a16:
            a21.append(ord(i))
        return a21

    def bytes2str(a10):
        a13 = 0
        a14 = len(a10)
        a15 = ''
        while True:
            if a13 >= a14:
                break
            a15 += chr(255 & a10[a13])
            a13 += 1
        return a15

    def digest_pad(a36):
        a41 = []
        a39 = 0
        a40 = len(a36)
        a43 = 15 - (a40 % 16)
        a41.append(a43)
        while a39 < a40:
            a41.append(a36[a39])
            a39 += 1
        a45 = a43
        while a45 > 0:
            a41.append(0)
            a45 -= 1
        return a41

    def blocks2bytes(a29):
        a34 = []
        a33 = 0
        a32 = len(a29)
        while a33 < a32:
            a34 += [255 & rshift(i32(a29[a33]).value, 24)]
            a34 += [255 & rshift(i32(a29[a33]).value, 16)]
            a34 += [255 & rshift(i32(a29[a33]).value, 8)]
            a34 += [255 & a29[a33]]
            a33 += 1
        return a34

    def bytes2blocks(a22):
        a27 = []
        a28 = 0
        a26 = 0
        a25 = len(a22)
        while True:
            a27.append(((255 & a22[a26]) << 24) & 0xFFFFFFFF)
            a26 += 1
            if a26 >= a25:
                break
            a27[a28] |= ((255 & a22[a26]) << 16 & 0xFFFFFFFF)
            a26 += 1
            if a26 >= a25:
                break
            a27[a28] |= ((255 & a22[a26]) << 8 & 0xFFFFFFFF)
            a26 += 1
            if a26 >= a25:
                break
            a27[a28] |= (255 & a22[a26])
            a26 += 1
            if a26 >= a25:
                break
            a28 += 1
        return a27

    def xor_blocks(a76, a77):
        return [a76[0] ^ a77[0], a76[1] ^ a77[1]]

    def unpad(a46):
        a49 = 0
        a52 = []
        a53 = (7 & a46[a49])
        a49 += 1
        a51 = (len(a46) - a53)
        while a49 < a51:
            a52 += [a46[a49]]
            a49 += 1
        return a52

    def rshift(a, b):
        return (a % 0x100000000) >> b

    def tea_code(a79, a80):
        a85 = a79[0]
        a83 = a79[1]
        a87 = 0

        for a86 in range(32):
            a85 += i32((((i32(a83).value << 4) ^ rshift(i32(a83).value, 5)) + a83) ^ (a87 + a80[(a87 & 3)])).value
            a85 = i32(a85 | 0).value
            a87 = i32(a87).value - i32(1640531527).value
            a83 += i32(
                (((i32(a85).value << 4) ^ rshift(i32(a85).value, 5)) + a85) ^ (a87 + a80[(rshift(a87, 11) & 3)])).value
            a83 = i32(a83 | 0).value
        return [a85, a83]

    def binarydigest(a55):
        a63 = [1633837924, 1650680933, 1667523942, 1684366951]
        a62 = [1633837924, 1650680933]
        a61 = a62
        a66 = [0, 0]
        a68 = [0, 0]
        a59 = bytes2blocks(digest_pad(str2bytes(a55)))
        a65 = 0
        a67 = len(a59)
        while a65 < a67:
            a66[0] = a59[a65]
            a65 += 1
            a66[1] = a59[a65]
            a65 += 1
            a68[0] = a59[a65]
            a65 += 1
            a68[1] = a59[a65]
            a65 += 1
            a62 = tea_code(xor_blocks(a66, a62), a63)
            a61 = tea_code(xor_blocks(a68, a61), a63)
            a64 = a62[0]
            a62[0] = a62[1]
            a62[1] = a61[0]
            a61[0] = a61[1]
            a61[1] = a64

        return [a62[0], a62[1], a61[0], a61[1]]

    def ascii2bytes(a99):
        a2b = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
               'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
               'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30,
               'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38, 'n': 39, 'o': 40,
               'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50,
               'z': 51, '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60,
               '9': 61, '-': 62, '_': 63}
        a6 = -1
        a7 = len(a99)
        a9 = 0
        a8 = []

        while True:
            while True:
                a6 += 1
                if a6 >= a7:
                    return a8
                if a99[a6] in a2b.keys():
                    break
            a8.insert(a9, i32(i32(a2b[a99[a6]]).value << 2).value)
            while True:
                a6 += 1
                if a6 >= a7:
                    return a8
                if a99[a6] in a2b.keys():
                    break
            a3 = a2b[a99[a6]]
            a8[a9] |= rshift(i32(a3).value, 4)
            a9 += 1
            a3 = (15 & a3)
            if (a3 == 0) and (a6 == (a7 - 1)):
                return a8
            a8.insert(a9, i32(a3).value << 4)
            while True:
                a6 += 1
                if a6 >= a7:
                    return a8
                if a99[a6] in a2b.keys():
                    break
            a3 = a2b[a99[a6]]
            a8[a9] |= rshift(i32(a3).value, 2)
            a9 += 1
            a3 = (3 & a3)
            if (a3 == 0) and (a6 == (a7 - 1)):
                return a8
            a8.insert(a9, i32(a3).value << 6)
            while True:
                a6 += 1
                if a6 >= a7:
                    return a8
                if a99[a6] in a2b.keys():
                    break
            a8[a9] |= a2b[a99[a6]]
            a9 += 1

        return a8

    def ascii2binary(a0):
        return bytes2blocks(ascii2bytes(a0))

    def tea_decode(a90, a91):
        a95 = a90[0]
        a96 = a90[1]
        a97 = i32(-957401312).value
        for a98 in range(32):
            a96 = i32(a96).value - ((((i32(a95).value << 4) ^ rshift(i32(a95).value, 5)) + a95) ^ (
                a97 + a91[(rshift(i32(a97).value, 11) & 3)]))
            a96 = i32(a96 | 0).value
            a97 = i32(a97).value + 1640531527
            a97 = i32(a97 | 0).value
            a95 = i32(a95).value - i32(
                (((i32(a96).value << 4) ^ rshift(i32(a96).value, 5)) + a96) ^ (a97 + a91[(a97 & 3)])).value
            a95 = i32(a95 | 0).value
        return [a95, a96]

    if data_seed is None or data_file is None:
        return ''

    data_seed = re.sub('[012567]', replacer, data_seed)
    new_data_seed = binarydigest(data_seed)
    new_data_file = ascii2binary(data_file)
    a69 = 0
    a70 = len(new_data_file)
    a71 = [1633837924, 1650680933]
    a73 = [0, 0]
    a74 = []
    while a69 < a70:
        a73[0] = new_data_file[a69]
        a69 += 1
        a73[1] = new_data_file[a69]
        a69 += 1
        a72 = xor_blocks(a71, tea_decode(a73, new_data_seed))
        a74 += a72
        a71[0] = a73[0]
        a71[1] = a73[1]
    return re.sub('[012567]', replacer, bytes2str(unpad(blocks2bytes(a74))))

# Credits to https://github.com/jmir1
key = "0wMrYU+ixjJ4QdzgfN2HlyIVAt3sBOZnCT9Lm7uFDovkb/EaKpRWhqXS5168ePcG"

def encode(input: str): return quote(input)
def decode(input: str): return unquote(input)

# ================================================================

def A_(input: str):
    output = ''
    for i in range(0, len(input), 3):
        a = [-1] * 4
        a[0] = ord(input[i]) >> 2
        a[1] = (3 & ord(input[i])) << 4
        if len(input) > i + 1:
            a[1] = a[1] | (ord(input[i+1]) >> 4)
            a[2] = (15 & ord(input[i+1])) << 2
        if len(input) > i + 2:
            a[2] = a[2] | (ord(input[i+2]) >> 6)
            a[3] = 63 & ord(input[i+2])
        for n in a:
            if n == -1: output += '='
            elif n in range(0, 64): output += key[n]
    return output    

# ================================================================

def B_(inputOne: str, inputTwo: str):
    arr = list(range(0,256))
    output, u = '', 0
    for a in range(0, len(arr)):
        u = (u + arr[a] + ord(inputOne[a % len(inputOne)])) % 256
        arr[a], arr[u] = arr[u], arr[a]
    u, c = 0, 0
    for f in range(0, len(inputTwo)):
        c = (c + f) % 256
        u = (u + arr[c]) % 256
        arr[c], arr[u] = arr[u], arr[c]
        output += chr(ord(inputTwo[f]) ^ arr[(arr[c] + arr[u]) % 256])
    return output

# ================================================================


def C_(input: str):
    t = input
    if len(re.sub('[\t\n\f\r]', '', input)) % 4 == 0:
        t = re.sub('==?$', '', input)
    if len(t) % 4 == 1 or len(re.findall('[^+/0-9A-Za-z]', t)):
        print('bad input')
        return
    r, e, u = '', 0, 0
    for o in range(0, len(t)):
        e, i = e << 6, key.index(t[o])
        e = e | i
        u += 6
        if 24 == u:
            r += chr((16711680 & e) >> 16)
            r += chr((65280 & e) >> 8)
            r += chr(255 & e)
            e, u = 0, 0
    if 12 == u:
        e = e >> 4
        return r + chr(e)
    else:
        if 18 == u:
            e = e >> 2
            r += chr((65280 & e) >> 8)
            r += chr(255 & e)
        return r
    
# ================================================================

def getVrf(id: str):
    reversed = A_(encode(id) + "0000000")[0:6][::-1]
    return re.sub('=+$', '', reversed + A_(B_(reversed, encode(id))))

# ================================================================

def getLink(url: str):
    i = url[0:6]
    n = url[6:]
    return decode(B_(i, C_(n)))

# ================================================================
