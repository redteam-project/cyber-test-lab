#!/usr/bin/env python3

import numpy as np
import scipy.stats as stats
import sys
import pylab as pl

# to make afCc.txt
# find ctl-results/fedora/27 -type f -exec grep afCc {} \; | grep -v null | awk '{print $2}' | sed -e 's/,$//' > afCc.txt

complexities = []
with open(sys.argv[1], 'r') as f:
	for line in f:
		if int(line) > 0:
			complexities.append(int(line))

textbox = 'cyclomatic complexity pdf for fedora 27 (incomplete)\n' + \
          'total: ' + str(len(complexities)) + '\n' + \
          'minimum: ' + str(min(complexities)) + '\n' + \
          'maximum:  ' + str(max(complexities)) + '\n' + \
          'mean: ' + str(np.mean(complexities)) + '\n' + \
          'median: ' + str(np.median(complexities)) + '\n' + \
          'mode: ' + str(stats.mode(complexities)) + '\n' + \
          'stdev: ' + str(np.std(complexities))

h = sorted(complexities)
fit = stats.norm.pdf(h, np.mean(h), np.std(h))
pl.plot(h,fit,'o')
pl.hist(h,normed=True)
pl.text(150, 0.0065, textbox, fontsize=9)
pl.show()
