# -*- coding : UTF-8 -*- #

# Copyright 2020 ws1004
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Contact : <ws1004@kakao.com // ws1004.4n6@gmail.com>

from datetime import datetime, timedelta
import binascii
import ctypes
import struct
import sys, os, io

def convert_bytes(obyte):           # One Byte to int
    return struct.unpack_from("B", obyte)[0]

def convert_word(tbytes):           # Two Byte to int
    return struct.unpack_from("H", tbytes)[0]

def convert_dword(fbytes):          # Four Byte to int
    return struct.unpack_from("I", fbytes)[0]

def convert_dwordlong(ebytes):      # Eight Byte to int
    return struct.unpack_from("Q", ebytes)[0]

def convert_string(nbytes, data):   # NByte to String
    thestring = struct.unpack_from("{}s".format(str(nbytes)), data)[0]
    thestring = thestring.decode('ascii', 'ignore')
    return thestring

def convert_timestamp(time):        # convert timestamp
    return str(datetime(1600,1,1) + timedelta(microseconds=time / 10.)) 

def create_filename(nbytes, data):
    filename = data.split(b"\x00\x00")[0]
    fdata = convert_string(len(filename), filename)
    return fdata.replace("\x00", "")

class prefetch_winxp(object):         # Windows XP Version
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.FileInformation_v17(FILE=FILE)
        self.strings = self.Strings(FILE=FILE, offset=self.string_info_offset, length=self.string_info_size)
        self.vol = self.Volumes(FILE=FILE, offset=self.volumes_info_offset)

    def FileHeader(self, FILE):     # Header is 84 Byte(0x54)
        F = FILE[0:84]
        self.version = convert_dword(F[0:4])
        self.signature = F[4:8]
        self.file_size = F[12:16]
        self.filename = create_filename(60,F[16:76])
        self.file_path_hash = convert_dword(F[76:80])

    def FileInformation_v17(self, FILE):    # File Infomation is 156 Byte(0x9C)
        F = FILE[84:240]
        self.file_metrics_array_info_offset = convert_dword(F[0:4])
        self.num_file_metrics_array = convert_dword(F[4:8])
        self.trace_chains_array_info_offset = convert_dword(F[8:12])
        self.num_trace_chains_array = convert_dword(F[12:16])
        self.string_info_offset = convert_dword(F[16:20])
        self.string_info_size = convert_dword(F[20:24])
        self.volumes_info_offset = convert_dword(F[24:28])
        self.num_volumes = convert_dword(F[28:32])
        self.volumes_info_size = convert_dword(F[32:36])
        self.last_launch_time = convert_dwordlong(F[36:44])
        self.runcount = convert_dword(F[60:64])

    def Strings(self, FILE, offset, length):    # Load File List is length Byte
        strings = []
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        result = strings_data.split("\x00\x00")

        for data in result:
            strings.append(data.replace("\x00",""))

        return strings

    def Volumes(self, FILE, offset):            # Volume Data
        result = []
        real_offset = offset
        F = FILE[offset:offset+96]
        for i in range(0, self.num_volumes):
            data = []
            data.append(convert_dword(F[0:4]))
            data.append(convert_dword(F[4:8]))
            data.append(convert_timestamp(convert_dwordlong(F[8:16])))
            data.append(str(hex(convert_dword(F[16:20])))[2:].upper())
            volume = FILE[(real_offset+data[0]):(real_offset+data[0]+(data[1] * 2))]
            data.append(create_filename(data[1]*2, volume))

            result.append(data)
            offset = offset+96
            F = FILE[offset:offset+96]
        return result

class prefetch_win7(object):         # Windows 7 Version
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.FileInformation_v23(FILE=FILE)
        self.strings = self.Strings(FILE=FILE, offset=self.string_info_offset, length=self.string_info_size)
        self.vol = self.Volumes(FILE=FILE, offset=self.volumes_info_offset)

    def FileHeader(self, FILE):     # Header is 84 Byte(0x54)
        F = FILE[0:84]
        self.version = convert_dword(F[0:4])
        self.signature = F[4:8]
        self.file_size = F[12:16]
        self.filename = create_filename(60,F[16:76])
        self.file_path_hash = convert_dword(F[76:80])

    def FileInformation_v23(self, FILE):    # File Infomation is 156 Byte(0x9C)
        F = FILE[84:240]
        self.file_metrics_array_info_offset = convert_dword(F[0:4])
        self.num_file_metrics_array = convert_dword(F[4:8])
        self.trace_chains_array_info_offset = convert_dword(F[8:12])
        self.num_trace_chains_array = convert_dword(F[12:16])
        self.string_info_offset = convert_dword(F[16:20])
        self.string_info_size = convert_dword(F[20:24])
        self.volumes_info_offset = convert_dword(F[24:28])
        self.num_volumes = convert_dword(F[28:32])
        self.volumes_info_size = convert_dword(F[32:36])
        self.last_launch_time = convert_dwordlong(F[44:52])
        self.runcount = convert_dword(F[68:72])
    
    def Strings(self, FILE, offset, length):    # Load File List is length Byte
        strings = []
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        result = strings_data.split("\x00\x00")

        for data in result:
            strings.append(data.replace("\x00",""))

        return strings

    def Volumes(self, FILE, offset):            # Volume Data
        result = []
        real_offset = offset
        F = FILE[offset:offset+96]
        for i in range(0, self.num_volumes):
            data = []
            data.append(convert_dword(F[0:4]))
            data.append(convert_dword(F[4:8]))
            data.append(convert_timestamp(convert_dwordlong(F[8:16])))
            data.append(str(hex(convert_dword(F[16:20])))[2:].upper())
            volume = FILE[(real_offset+data[0]):(real_offset+data[0]+(data[1] * 2))]
            data.append(create_filename(data[1]*2, volume))

            result.append(data)
            offset = offset+96
            F = FILE[offset:offset+96]
        return result

class prefetch_win8(object):         # Windows 8.1 Version
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.FileInformation_v26(FILE=FILE)
        self.strings = self.Strings(FILE=FILE, offset=self.string_info_offset, length=self.string_info_size)
        self.vol = self.Volumes(FILE=FILE, offset=self.volumes_info_offset)
    
    def FileHeader(self, FILE):     # Header is 84 Byte(0x54)
        F = FILE[0:84]
        self.version = convert_dword(F[0:4])
        self.signature = F[4:8]
        self.file_size = F[12:16]
        self.filename = create_filename(60,F[16:76])
        self.file_path_hash = convert_dword(F[76:80])

    def FileInformation_v26(self, FILE):
        F = FILE[84:240]
        self.file_metrics_array_info_offset = convert_dword(F[0:4])
        self.num_file_metrics_array = convert_dword(F[4:8])
        self.trace_chains_array_info_offset = convert_dword(F[8:12])
        self.num_trace_chains_array = convert_dword(F[12:16])
        self.string_info_offset = convert_dword(F[16:20])
        self.string_info_size = convert_dword(F[20:24])
        self.volumes_info_offset = convert_dword(F[24:28])
        self.num_volumes = convert_dword(F[28:32])
        self.volumes_info_size = convert_dword(F[32:36])
        self.last_launch_time = convert_dwordlong(F[44:52])
        self.launch_time = struct.unpack("7Q",F[52:108])
        self.runcount = convert_dword(F[124:128])
    
    def Strings(self, FILE, offset, length):    # Load File List is length Byte
        strings = []
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        result = strings_data.split("\x00\x00")

        for data in result:
            strings.append(data.replace("\x00",""))

        return strings   

    def Volumes(self, FILE, offset):            # Volume Data
        result = []
        real_offset = offset
        F = FILE[offset:offset+96]
        for i in range(0, self.num_volumes):
            data = []
            data.append(convert_dword(F[0:4]))
            data.append(convert_dword(F[4:8]))
            data.append(convert_timestamp(convert_dwordlong(F[8:16])))
            data.append(str(hex(convert_dword(F[16:20])))[2:].upper())
            volume = FILE[(real_offset+data[0]):(real_offset+data[0]+(data[1] * 2))]
            data.append(create_filename(data[1]*2, volume))

            result.append(data)
            offset = offset+96
            F = FILE[offset:offset+96]
        return result
    

class prefetch_win10(object):         # Windows 10 Version
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.FileInformation_v30(FILE=FILE)
        self.strings = self.Strings(FILE=FILE, offset=self.string_info_offset, length=self.string_info_size)
        self.vol = self.Volumes(FILE=FILE, offset=self.volumes_info_offset)

    def FileHeader(self, FILE):     # Header is 84 Byte(0x54)
        F = FILE[0:84]
        self.version = convert_dword(F[0:4])
        self.signature = F[4:8]
        self.file_size = F[12:16]
        self.filename = create_filename(60,F[16:76])
        self.file_path_hash = convert_dword(F[76:80])

    def FileInformation_v30(self, FILE):    # File Infomation is 156 Byte(0x9C)
        F = FILE[84:240]
        self.file_metrics_array_info_offset = convert_dword(F[0:4])
        self.num_file_metrics_array = convert_dword(F[4:8])
        self.trace_chains_array_info_offset = convert_dword(F[8:12])
        self.num_trace_chains_array = convert_dword(F[12:16])
        self.string_info_offset = convert_dword(F[16:20])
        self.string_info_size = convert_dword(F[20:24])
        self.volumes_info_offset = convert_dword(F[24:28])
        self.num_volumes = convert_dword(F[28:32])
        self.volumes_info_size = convert_dword(F[32:36])
        self.last_launch_time = convert_dwordlong(F[44:52])
        self.launch_time = struct.unpack("7Q",F[52:108])
        self.runcount = convert_dword(F[124:128])
        
    def Strings(self, FILE, offset, length):    # Load File List is length Byte
        strings = []
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        result = strings_data.split("\x00\x00")

        for data in result:
            strings.append(data.replace("\x00",""))

        return strings        

    def Volumes(self, FILE, offset):            # Volume Data
        result = []
        real_offset = offset
        F = FILE[offset:offset+96]

        for i in range(0, self.num_volumes):
            data = []
            data.append(convert_dword(F[0:4]))
            data.append(convert_dword(F[4:8]))
            data.append(convert_timestamp(convert_dwordlong(F[8:16])))
            data.append(str(hex(convert_dword(F[16:20])))[2:].upper())
            volume = FILE[(real_offset+data[0]):(real_offset+data[0]+(data[1] * 2))]
            data.append(create_filename(data[1]*2, volume))

            result.append(data)
            
            offset = offset+96
            F = FILE[offset:offset+96]
        return result

# This is Picasso's w10pfdecomp.py script.
# 
# Author's name: Francesco "dfirfpi" Picasso
# Author's email: francesco.picasso@gmail.com
# 
# Source: https://github.com/dfirfpi/hotoloti/blob/master/sas/w10pfdecomp.py
# License: http://www.apache.org/licenses/LICENSE-2.0

class DecompressWin10(object):
    def __init__(self):
        pass

    def tohex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress(self, FILE):
        NULL = ctypes.POINTER(ctypes.c_uint)()
        SIZE_T = ctypes.c_uint
        DWORD = ctypes.c_uint32
        USHORT = ctypes.c_uint16
        UCHAR = ctypes.c_ubyte
        ULONG = ctypes.c_uint32

        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
        except AttributeError:
            sys.exit('You must have Windows with version >=8.')

        RtlGetCompressionWorkSpaceSize = \
            ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

        with open(FILE, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()

            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF
            if magic != 0x004d414d:
                sys.exit('Wrong signature... wrong file?')

            if crcck:
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L', 0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)
                if crc != file_crc:
                    sys.exit('{} Wrong file CRC {0:x} - {1:x}!'.format(FILE, crc, file_crc))

            compressed_size = len(compressed)

            ntCompressBufferWorkSpaceSize = ULONG()
            ntCompressFragmentWorkSpaceSize = ULONG()

            ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                       ctypes.byref(ntCompressBufferWorkSpaceSize),
                       ctypes.byref(ntCompressFragmentWorkSpaceSize))

            if ntstatus:
                sys.exit('Cannot get workspace size, err: {}'.format(
                    self.tohex(ntstatus, 32)))

            ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (UCHAR * decompressed_size)()
            ntFinalUncompressedSize = ULONG()
            ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()

            ntstatus = RtlDecompressBufferEx(
                USHORT(calgo),
                ctypes.byref(ntDecompressed),
                ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))

            if ntstatus:
                sys.exit('Decompression failed, err: {}'.format(tohex(ntstatus, 32)))

            if ntFinalUncompressedSize.value != decompressed_size:
                sys.exit('Decompressed with a different size than original!')

        return bytearray(ntDecompressed)

def print_data(FILE):
    with open(FILE, "rb") as d:
        f = d.read()
        version = convert_dword(f[0:4])
        if version == 17:           # windows xp pf file
            p = prefetch_winxp(bytearray(f))
        elif version == 23:         # windows 7 pf file
            p = prefetch_win7(bytearray(f))
        elif version == 26:         # windows 8 pf file
            p = prefetch_win8(bytearray(f))
        elif version == 30:         # windows 10 pf file(Decompress_File)
            p = prefetch_win10(bytearray(f))
        else:                       # windows 10 pf file(Undecompress_File)
            compressedHeader = convert_string(3, f[0:3])
            if compressedHeader == 'MAM':
                d = DecompressWin10()
                decompressed = d.decompress(FILE)
                p = prefetch_win10(decompressed)
            else:
                print("[ - ] {} is not valid PF File".format(FILE))
                return

    line = "=" * (len(p.filename) + 2)
    print("{0}\n {1} \n{0}\n".format(line,p.filename))
    print("File Path Hash : {}".format(str(hex(p.file_path_hash))[2:].upper()))
    print("File Size : {}".format(convert_dword(p.file_size)))
    print("Run Count : {}\n".format(p.runcount))
    print("Last Executed Time : {}".format(convert_timestamp(p.last_launch_time)))
    
    if hasattr(p, "launch_time"):
        print("Launch Time : ")
        for data in p.launch_time:
            if data:
                print("└  {}".format(convert_timestamp(data)))
    
    for data in p.vol:
        print("\nVolume path : {}".format(data[4]))
        print("Volume Serial Number : {}".format(data[3]))

    print("\nRoad File List : ")
    
    count = 1

    for data in p.strings:
        if data != p.strings[-1]:
            if count > 999:
                print("{}: {}".format(count, data))
            elif count > 99:
                print("{}:  {}".format(count, data))
            elif count > 9:
                print("{}:   {}".format(count, data))
            else:
                print("{}:    {}".format(count, data))
        count += 1

    print("\n\n")

def main():
    if sys.version_info > (3, 8, 0):
        if len(sys.argv) != 2:
            sys.exit("Command : python {} [FILE]".format(sys.argv[0]))
        else:
            if os.path.isfile(sys.argv[1]):
                if os.path.getsize(sys.argv[1]) > 0:
                    print_data(sys.argv[1])
                    pass
            if os.path.isdir(sys.argv[1]):
                if not (sys.argv[1].endswith("/") or sys.argv[1].endswith("\\")):
                    sys.exit("[ - ] Add a trailing slash\n[ - ] Example : [DIRECTORY]\\ or [DIRECTORY]/")
                for pfile in os.listdir(sys.argv[1]):
                    if pfile.endswith(".pf"):
                        if os.path.getsize(sys.argv[1] + pfile) > 0:
                            print_data(sys.argv[1] + pfile)
    else:
        sys.exit("Using Python Version 3.8.0 or later to run this script")

if __name__ == "__main__":
    main()