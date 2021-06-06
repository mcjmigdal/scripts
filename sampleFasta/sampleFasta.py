#!/usr/bin/env python2.7
# By Migdal Warsaw May 2018

from Bio.SeqIO.QualityIO import FastqGeneralIterator
from sys import argv
import random
import gzip

fastq = gzip.open(argv[1],  "rt")
threshold = float(argv[2])
adapter_p = float(argv[3])

adapter= "CTGTCTCTTATACACATCT"
adapter_len = len(adapter)

def draw(threshold=0.5):
    if random.random() <= threshold:
        return True
    else:
        return False

def addAdapter(seq, adapter, adapter_len, p):
    '''Substitutes the 3' end of sequencing read for given adapter sequence with prob. eq. p'''
    if random.random() <= p:
        cut = random.randint(0,adapter_len-1)
        return seq[:-(adapter_len - cut)] + adapter[:(adapter_len - cut)]
    else:
        return seq

for name, seq, qual in FastqGeneralIterator(fastq):
    if draw(threshold):
        print "@" + name
        print addAdapter(seq, adapter, adapter_len, adapter_p)
        print "+" + name
        print qual
