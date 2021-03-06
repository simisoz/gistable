#! /usr/bin/env python
 
# Copyright (C) 2008-2009 by Guy Rutenberg
 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 
import hashlib
import tarfile
 
def tarsum(input_file, hash, output_file):
        """
        input_file  - A FILE object to read the tar file from.
        hash - The name of the hash to use. Must be supported by hashlib.
        output_file - A FILE to write the computed signatures to.
        """
        tar = tarfile.open(mode="r|*", fileobj=input_file)
 
        chunk_size = 100*1024
        store_digests = {}
 
        for member in tar:
            if not member.isfile():
                continue
            f = tar.extractfile(member)
            h = hashlib.new(hash)
            data = f.read(chunk_size)
            while data:
                h.update(data)
                data = f.read(chunk_size)
            output_file.write("%s  %s\n" % (h.hexdigest(), member.name))
 
def main():
    parser = OptionParser()
 
    version=("%prog 0.2.1\n"
             "Copyright (C) 2008-2009 Guy Rutenberg <http://www.guyrutenberg.com/contact-me>")
    usage=("%prog [options] TARFILE\n"
           "Print a checksum signature for every file in TARFILE.\n"
           "With no FILE, or when FILE is -, read standard input.")
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-c", "--checksum", dest="checksum", type="string",
        help="use HASH as for caclculating the checksums. [default: %default]", metavar="HASH",
        default="md5")
    parser.add_option("-o", "--output", dest="output", type="string",
        help="save signatures to FILE.", metavar="FILE")
 
    (option, args) = parser.parse_args()
 
    output_file = sys.stdout
    if option.output:
        output_file = open(option.output, "w")
 
    input_file = sys.stdin
    if len(args)==1 and args[0]!="-":
        input_file = open(args[0], "r")
 
    tarsum(input_file, option.checksum, output_file)
 
if __name__ == "__main__":
    from optparse import OptionParser
    import sys
    main()