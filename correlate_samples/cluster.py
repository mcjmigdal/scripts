#!/usr/bin/env python2.7
#By Migdal 24/03/17
description='''Takes bed from bedtools coverage and test different samples for 
correlation. Might cluster also if more than two samples are given'''
from scipy.stats import pearsonr
import argparse
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

class bedVector(object):
	def __init__(self, bedfile, split_by_chromosome=False,normalize=True):
		self.vec = []
		self.window = 0
		with open(bedfile) as bed:
			line = bed.readline().strip().split()
			self.window += int(line[2]) - int(line[1])
			while line:
				count = int(line[3])
				self.vec.append( count )
				line = bed.readline().strip().split()
		if normalize:
			total = sum(self.vec)
			self.vec = [ float(x)/total for x in self.vec ]

	def __str__(self):
		return ','.join([ str(c) for c in self.vec])

	def __iter__(self):
		return iter(self.vec)

	def R(self,vecB):
		r, p = pearsonr(self.vec,vecB.vec)
		return r, p

def main():
	parser = argparse.ArgumentParser(description)
	parser.add_argument('vectors', help='''vec1.bed vec2.bed 
			     [vec3.bed ...]''', nargs='+')
	parser.add_argument('--no_corr', action='store_false', \
					help='don\'t calculate pearson correlation between samples')
	parser.add_argument('--histogram', action='store_true', \
					help='cluster and plot histogram')
        args = parser.parse_args()

	vectors = [ bedVector(v) for v in args.vectors ]
#	R = {}
#	for i, v in enumerate(args.vectors):
#		#Brute force solution, most values are computted multiple times
#		R[v] = [ vectors[i].R(vecB)[0] for vecB in vectors ]
#	
#	print pd.DataFrame(data=R, index=args.vectors)

	if args.no_corr:
		R = []
		for i, v in enumerate(args.vectors):
			r = [ vectors[i].R(vecB)[0] for vecB in vectors[i:] ]
			r_prev = [ vec[i] for vec in R[:i] ]
			R.append( r_prev + r )
	
		print pd.DataFrame(data=R, columns=[ v.split('/')[-1][:9] for v in args.vectors], \
							index=[ v.split('/')[-1][:9] for v in args.vectors])
	if args.histogram:
		m, me = 'single', 'correlation'
		X = np.array([ v.vec for v in vectors])
		Z = linkage(X, method=m, metric=me)
		print cophenet(Z, pdist(X,metric=me))

		import matplotlib.pyplot as plt
		dendrogram(
    			Z,
    			leaf_rotation=90.,  # rotates the x axis labels
    			leaf_font_size=8.,  # font size for the x axis labels
			labels=[ v.split('/')[-1][:9] for v in args.vectors],
			)
		plt.savefig('histogram.png')
#		plt.show()

if __name__ == '__main__':
	main()
	
