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
import struct
import sys, string

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

class recycle_bin_winXP(object):
    def __init__(self, FILE):
        self.filedata = self.FileData(FILE=FILE)
        
    def FileData(self, FILE):
        self.version = str(convert_dword(FILE[0:4]))+" (Windows XP)"
        self.info2_filesize = len(FILE)
        self.entry_size = convert_dword(FILE[12:16])

        result = []
        offset = 0
        F = FILE[offset:offset+self.entry_size]
        for i in range(0, self.info2_filesize//self.entry_size):
            data = []
            if F[20] == 0x00:        # Not Remain in Recycle Bin
                self.remain = "No"
            else:                           # Remain in Recycle Bin
                self.remain = "YES"
            data.append(convert_dword(F[280:284]))                              # Index
            data.append(convert_timestamp(convert_dwordlong(F[288:296])))       # Deleted Time
            data.append(self.remain)                                            # Remain in RB
            data.append(convert_dword(F[296:300]))                              # File Size
            
            strings_data = convert_string(len(F[300::]), F[300::])
            data.append(strings_data.replace("\x00",""))
            result.append(data)
            offset = offset + self.entry_size
            F = FILE[offset:offset+self.entry_size]

        self.path_len = 0
        for i in range(0, (self.info2_filesize//self.entry_size)-1):
                if self.path_len <= len(result[i][4]):
                    self.path_len = len(result[i][4])

        return result
    
class recycle_bin_win78(object):
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.deleted_file_name = self.FileName(FILE=FILE, offset=24, length=520)

    def FileHeader(self, FILE):
        F = FILE[0:28]
        self.version = str(convert_dwordlong(F[0:8]))+" (Windows 78)"
        self.deleted_file_size = str(convert_dwordlong(F[8:16]))+" Byte"
        self.deleted_file_time = convert_timestamp(convert_dwordlong(F[16:24]))

    def FileName(self, FILE, offset, length):
        strings = ""
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        strings += strings_data.replace("\x00","")

        return strings

class recycle_bin_win10(object):
    def __init__(self, FILE):
        self.FileHeader(FILE=FILE)
        self.deleted_file_name = self.FileName(FILE=FILE, offset=28, length=self.deleted_file_name_size)

    def FileHeader(self, FILE):
        F = FILE[0:28]
        self.version = str(convert_dwordlong(F[0:8]))+" (Windows 10)"
        self.deleted_file_size = str(convert_dwordlong(F[8:16]))+" Byte"
        self.deleted_file_time = convert_timestamp(convert_dwordlong(F[16:24]))
        self.deleted_file_name_size = convert_dword(F[24:28])*2

    def FileName(self, FILE, offset, length):
        strings = ""
        F = FILE[offset:offset+length]
        strings_data = convert_string(length, F)
        strings += strings_data.replace("\x00","")

        return strings

def print_data(FILE):
    with open(FILE, "rb") as f:
        data = f.read()
        version = convert_dwordlong(data[0:8])
        if version == 1:            # windows 7 or windows 8.1
            r = recycle_bin_win78(bytearray(data))
            print("Command Line : python {} {}\n".format(sys.argv[0],sys.argv[1]))        
            print("Source File : {}\n".format(sys.argv[1]))
            
            if len(r.deleted_file_name) > len(r.deleted_file_time):
                print("┌"+"───────────────────"+"─"*(len(r.deleted_file_name))+"─┐")
                print("│ Version: {}".format(r.version)+" "*(len(r.deleted_file_name)-4)+"│")
                print("│ Deleted File Size: {}".format(r.deleted_file_size)+" "*(len(r.deleted_file_name)-len(r.deleted_file_size))+"│")
                print("│ Deleted File Name: {}│".format(r.deleted_file_name))
                print("│ Deleted File Time: {}".format(r.deleted_file_time)+" "*(len(r.deleted_file_name)-len(r.deleted_file_time))+"│")
                print("└"+"───────────────────"+"─"*(len(r.deleted_file_name))+"─┘")
            else:
                print("┌"+"───────────────────"+"─"*(len(r.deleted_file_time))+"─┐")
                print("│ Version: {}".format(r.version)+" "*(len(r.deleted_file_time)-4)+"│")
                print("│ Deleted File Size: {}".format(r.deleted_file_size)+" "*(len(r.deleted_file_time)-len(r.deleted_file_size))+"│")
                print("│ Deleted File Name: {}".format(r.deleted_file_name)+" "*(len(r.deleted_file_time)-len(r.deleted_file_name))+"│")
                print("│ Deleted File Time: {}".format(r.deleted_file_time)+" "*(len(r.deleted_file_name)-len(r.deleted_file_time))+"│")
                print("└"+"───────────────────"+"─"*(len(r.deleted_file_time))+"─┘")
        elif version == 2:          # windows 10
            r = recycle_bin_win10(bytearray(data))
            print("Command Line : python {} {}\n".format(sys.argv[0],sys.argv[1]))        
            print("Source File : {}\n".format(sys.argv[1]))
            
            if len(r.deleted_file_name) > len(r.deleted_file_time):
                print("┌"+"───────────────────"+"─"*(len(r.deleted_file_name))+"─┐")
                print("│ Version: {}".format(r.version)+" "*(len(r.deleted_file_name)-4)+"│")
                print("│ Deleted File Size: {}".format(r.deleted_file_size)+" "*(len(r.deleted_file_name)-len(r.deleted_file_size))+"│")
                print("│ Deleted File Name: {}│".format(r.deleted_file_name))
                print("│ Deleted File Time: {}".format(r.deleted_file_time)+" "*(len(r.deleted_file_name)-len(r.deleted_file_time))+"│")
                print("└"+"───────────────────"+"─"*(len(r.deleted_file_name))+"─┘")
            else:
                print("┌"+"───────────────────"+"─"*(len(r.deleted_file_time))+"─┐")
                print("│ Version: {}".format(r.version)+" "*(len(r.deleted_file_time)-4)+"│")
                print("│ Deleted File Size: {}".format(r.deleted_file_size)+" "*(len(r.deleted_file_time)-len(r.deleted_file_size))+"│")
                print("│ Deleted File Name: {}".format(r.deleted_file_name)+" "*(len(r.deleted_file_time)-len(r.deleted_file_name))+"│")
                print("│ Deleted File Time: {}".format(r.deleted_file_time)+" "*(len(r.deleted_file_name)-len(r.deleted_file_time))+"│")
                print("└"+"───────────────────"+"─"*(len(r.deleted_file_time))+"─┘")
        else:                       # windows XP
            r = recycle_bin_winXP(bytearray(data))
            print("Command Line : python {} {}\n".format(sys.argv[0],sys.argv[1]))        
            print("Source File : {}\n".format(sys.argv[1]))
            print("Version: {}".format(r.version))
            print("Time zone: Coordinated Universal Time [UTC+0]\n")
            
            print("┌"+"─────────────────────────────────────────────────────────────────"+"─"*(r.path_len)+"─┐")
            print("│ Index | Deleted Time               | Remain in RB | File Size | Path"+" "*(r.path_len-4)+" │")
            for data in r.filedata:
                print("│ {0:<5} | {1:<26} | {2:<12} | {3:<9} | {4:<{5}} │".format(data[0],data[1],data[2],data[3],data[4],r.path_len))
            print("└"+"─────────────────────────────────────────────────────────────────"+"─"*(r.path_len)+"─┘")

def main():
    print("RBParser version 1.0.0\n")
    print("Author: ws1004 (ws1004@kakao.com)")
    print("https://github.com/ws1004-4n6/Tool-development/tree/master/$Recycle_Bin_Parser\n")
    if sys.version_info > (3, 8, 0):
        if len(sys.argv) != 2:
            sys.exit("Example : python {0} [INFO2 FILE]\n          python {0} [$I###### FILE]".format(sys.argv[0]))
        else:
            print_data(sys.argv[1])
    else:
        sys.exit("Using Python Version 3.8.0 or later to run this script")

if __name__ == "__main__":
    main()