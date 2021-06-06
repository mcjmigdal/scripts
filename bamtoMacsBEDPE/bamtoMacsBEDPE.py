#!/usr/bin/env python2.7
#By Migdal 25/06/17 Wroclaw-->Warsaw
description ='''Converts bam directly to BEDPE file format used by macs2, 
additonally allows to shits reads by arbitraly chosen number of bases in
strand aware manner'''

import pysam
from tempfile import NamedTemporaryFile
from os import remove
import argparse

def main():
	parser = argparse.ArgumentParser(epilog=description)
	parser.add_argument('bam', \
		help='input file to process')
	parser.add_argument('--shift', nargs=2, type=int, default=(0,0), \
		help='shift reads on + and - strands by shift1, shift2 [0 0]')
	parser.add_argument('--out_format', nargs=1, type=str, default='MBEDPE', \
		help='output file format [MBEDPE]')
	parser.add_argument("--nofilter", action='store_false', \
		help='do not filter input files (samtools view -b -f 2 -F 4 -F 8 -F 512 -F 256 -F 2048)')
	parser.add_argument("--sort", action='store_true', \
		help='sort input file by name, required if unsorted input is used')

	args = parser.parse_args()

	bam2bedpe(args.bam, oformat=args.out_format, shift=args.shift, \
		filter=args.nofilter, sort=args.sort)
	

def bam2bedpe(bam_name, oformat='MBEDPE', shift=(0,0), filter=True, sort=True):
	'''bam_name - path to bam file to process;
oformat - output format, available options are: MBEDPE (BEDPE format used by macs2);
shift - number of bases to shift read on [+,-] strands;
filter - fancy filtration criteria from macs2 (samtools view -b -f 2 -F 4 -F 8 -F 512 -F 256
-F 2048);
sort - bam file have to be sorted by name, if set to True will sort given alignment file to tmp file that will be
deleted after program completition'''
	template = { 'MBEDPE' : '%s\t%i\t%i' }[oformat]
	if sort:
		tmp = NamedTemporaryFile(delete=False)
		pysam.sort('-n','-o',tmp.name,bam_name)
		bam_name = tmp.name
		tmp.close()
		
	bam = pysam.AlignmentFile(bam_name)
	while bam:
		try:
			pair = [ bam.next() for i in range(2) ]
		except:
			break

		if not pair[0].qname == pair[1].qname:
			print 'Read %s out of order or file is not sorted' % (pair[1].qname)
			continue

		if filter:
			if not all( (pair[0].is_proper_pair, not(pair[0].is_unmapped), \
				not(pair[0].mate_is_unmapped), not(pair[0].is_qcfail), \
				not(pair[0].is_secondary), not(pair[0].is_supplementary)) ) \
			   and not all( (not(pair[0].is_qcfail), not(pair[0].is_secondary), \
					not(pair[0].is_supplementary)) ):
				 continue

		first = not( pair[0].pos < pair[1].pos )
		first = int( first )
		ref, pos1, qlen = pair[first].reference_name, pair[first].pos, \
					abs(pair[first].template_length)
		pos2 = pos1 + qlen
		if pair[first].is_reverse:
			pos1 += shift[1]
			pos2 += shift[0]
		else:
			pos1 += shift[0]
			pos2 += shift[1]

		print template % (ref,pos1,pos2)

	if sort:
		remove(tmp.name)

if __name__ == '__main__':
	main()
		

#qlen=3
#1 2 3 4 5
#  a a a
#
#2+3-1 = 4	???
#4-2+1 = 3	???
