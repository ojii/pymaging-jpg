# -*- coding: utf-8 -*-
# Copyright (c) 2013, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from collections import defaultdict
import os
import q


EOI = 0xFFD9
SOS = 0xFFDA
SOI = 0xFFD8
DHT = 0xFFC4

SEGMENT_NAMES = {}
SEGMENT_NAMES[0x00] = "Baseline DCT; Huffman"
SEGMENT_NAMES[0x01] = "Extended sequential DCT; Huffman"
SEGMENT_NAMES[0x02] = "Progressive DCT; Huffman"
SEGMENT_NAMES[0x03] = "Spatial lossless; Huffman"
SEGMENT_NAMES[0x04] = "Huffman table"
SEGMENT_NAMES[0x05] = "Differential sequential DCT; Huffman"
SEGMENT_NAMES[0x06] = "Differential progressive DCT; Huffman"
SEGMENT_NAMES[0x07] = "Differential spatial; Huffman"
SEGMENT_NAMES[0x08] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x09] = "Extended sequential DCT; Arithmetic"
SEGMENT_NAMES[0x0A] = "Progressive DCT; Arithmetic"
SEGMENT_NAMES[0x0B] = "Spatial lossless; Arithmetic"
SEGMENT_NAMES[0x0C] = "Arithmetic coding conditioning"
SEGMENT_NAMES[0x0D] = "Differential sequential DCT; Arithmetic"
SEGMENT_NAMES[0x0E] = "Differential progressive DCT; Arithmetic"
SEGMENT_NAMES[0x0F] = "Differential spatial; Arithmetic"
SEGMENT_NAMES[0x10] = "Restart"
SEGMENT_NAMES[0x11] = "Restart"
SEGMENT_NAMES[0x12] = "Restart"
SEGMENT_NAMES[0x13] = "Restart"
SEGMENT_NAMES[0x14] = "Restart"
SEGMENT_NAMES[0x15] = "Restart"
SEGMENT_NAMES[0x16] = "Restart"
SEGMENT_NAMES[0x17] = "Restart"
SEGMENT_NAMES[0x18] = "Start of image"
SEGMENT_NAMES[0x19] = "End of image"
SEGMENT_NAMES[0x1A] = "Start of scan"
SEGMENT_NAMES[0x1B] = "Quantisation table"
SEGMENT_NAMES[0x1C] = "Number of lines"
SEGMENT_NAMES[0x1D] = "Restart interval"
SEGMENT_NAMES[0x1E] = "Hierarchical progression"
SEGMENT_NAMES[0x1F] = "Expand reference components"
SEGMENT_NAMES[0x20] = "JFIF header"
SEGMENT_NAMES[0x21] = "[Reserved: application extension]"
SEGMENT_NAMES[0x22] = "[Reserved: application extension]"
SEGMENT_NAMES[0x23] = "[Reserved: application extension]"
SEGMENT_NAMES[0x24] = "[Reserved: application extension]"
SEGMENT_NAMES[0x25] = "[Reserved: application extension]"
SEGMENT_NAMES[0x26] = "[Reserved: application extension]"
SEGMENT_NAMES[0x27] = "[Reserved: application extension]"
SEGMENT_NAMES[0x28] = "[Reserved: application extension]"
SEGMENT_NAMES[0x29] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2A] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2B] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2C] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2D] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2E] = "[Reserved: application extension]"
SEGMENT_NAMES[0x2F] = "[Reserved: application extension]"
SEGMENT_NAMES[0x30] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x31] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x32] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x33] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x34] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x35] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x36] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x37] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x38] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x39] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x3A] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x3B] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x3C] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x3D] = "[Reserved: JPEG extension]"
SEGMENT_NAMES[0x3E] = "Comment"
SEGMENT_NAMES[0x3F] = "[Invalid]"


@q.t
def fgetc(fp):
        return ord(fp.read(1))

@q.t
def READ_WORD(fp):
    return (fgetc(fp) << 8) | fgetc(fp)


@q.t
def dht(fp, huff_data):
    ctr = 0
    code = 0
    table = fgetc(fp)
    ctr += 1
    counts = []
    for i in range(16):
        counts.append(fgetc(fp))
        ctr += 1
    for i in range(16):
        for j in range(counts[i]):
            huff_data[table][(i + 1, code)] = fgetc(fp)
            code += 1
            ctr += 1
        code <<= 1
    return ctr


@q.t
def parse_segments(fp, huff_data):
    while True:
        fpos = fp.tell()
        segment = READ_WORD(fp)

        q.q(hex(segment))

        if segment < 0xFFC0:
            raise ValueError("Segment ID expected, not found (%r)" % segment)

        yield segment, fpos

        if segment == EOI:
            q.q("EOI")
            raise StopIteration()
        elif segment == SOS:
            q.q("SOS")
            fp.seek(-2, os.SEEK_END)
        elif segment == SOI:
            q.q("SOI")
        elif segment == DHT:
            q.q("DHT")
            size = READ_WORD(fp) - 2;
            end_of_dht = dht(fp, huff_data)
            if end_of_dht != size:
                raise ValueError("Unexpected end of DHT (%s, expected %s)" % (end_of_dht, size))
        else:
            size = READ_WORD(fp)
            fp.seek(size - 2, os.SEEK_CUR)

@q.t
def main(fp):
    huff_data = defaultdict(dict)
    for segment, pos in parse_segments(fp, huff_data):
        print "Found segment %s at %s" % (SEGMENT_NAMES[segment - 0xFFC0], pos)

    print "Huffman Tables:"
    for key, value in huff_data.items():
        print '  %s:' % key
        for subkey, subvalue in value.items():
            print '    %s: %s' % subkey, subvalue


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as fp:
        main(fp)
