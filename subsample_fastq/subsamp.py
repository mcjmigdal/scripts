#!/usr/bin/env python
import argparse
from Bio.SeqIO.QualityIO import FastqGeneralIterator
import gzip
from pathlib import Path
import random

description = """
Subsample fastq.gz files
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument("R1", type=Path,
                    help="Forward reads file in fastq.gz format")
parser.add_argument("R1_out", type=str,
                    help="Output file for forward reads in fastq.gz format")
parser.add_argument("R2", type=Path, nargs="?",
                    help="Reverse reads file in fastq.gz format")
parser.add_argument("R2_out", type=str, nargs="?",
                    help="Output file for reverse reads in fastq.gz format")
parser.add_argument("--frac", type=float, required=True,
                    help="Float between 0.0 and 1.0 specifing fraction of reads to take")
parser.add_argument("--seed", type=int, default=9234322,
                    help="Integer seed for random number generator")
args = parser.parse_args()

if bool(args.R2) ^ bool(args.R2_out):
  raise ValueError("Both R2 and R2_out need to be specified")

random.seed(args.seed)
rd_state = random.getstate()
R1_n = 0
with gzip.open(args.R1, "rt") as handle, gzip.open(args.R1_out, "wt") as outfile:
  for record in FastqGeneralIterator(handle):
    R1_n += 1
    if random.random() < args.frac:
      outfile.write("@%s\n%s\n+\n%s\n" % (record))

if args.R2 and args.R2_out:
  random.setstate(rd_state)
  R2_n = 0
  with gzip.open(args.R2, "rt") as handle, gzip.open(args.R2_out, "wt") as outfile:
    for record in FastqGeneralIterator(handle):
      R2_n += 1
      if random.random() < args.frac:
        outfile.write("@%s\n%s\n+\n%s\n" % (record))

if (args.R2 and args.R2_out) and (R1_n != R2_n):
  raise ValueError("%s and %s has different number of records" % (R1, R2))
