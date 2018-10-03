#!/usr/bin/env python3
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from sys import argv
import gzip

if not len(argv) == 2:
    print("""Usage: fastq2fasta.py fastq.gz""")

try:
    with gzip.open(argv[1], 'rt') as handle:
        for title, seq, qual in FastqGeneralIterator(handle):
            print(">" + title)
            print(seq)
except OSError:
    print("Input fastq file have to be gzipped!")
