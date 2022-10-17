# Subsample reads from gzipped FASTQ files

## USAGE
```
usage: subsamp.py [-h] --frac FRAC [--seed SEED] R1 R1_out [R2] [R2_out]

Subsample fastq.gz files

positional arguments:
  R1           Forward reads file in fastq.gz format
  R1_out       Output file for forward reads in fastq.gz format
  R2           Reverse reads file in fastq.gz format
  R2_out       Output file for reverse reads in fastq.gz format

options:
  -h, --help   show this help message and exit
  --frac FRAC  Float between 0.0 and 1.0 specifing fraction of reads to take
  --seed SEED  Integer seed for random number generator
```

## TEST
`./subsamp.py --frac 0.2 R1.fastq.gz R1.sub.fastq.gz R2.fastq.gz R2.sub.fastq.gz`
