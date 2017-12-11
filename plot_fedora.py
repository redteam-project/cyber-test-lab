#!/usr/bin/env python

import numpy as np
import scipy.stats as stats
import sys
import pylab as pl
import json

with open(sys.argv[1], 'r') as f:
    jsondata = json.load(f)

package_scores = []
binary_scores = []
for package in jsondata.keys():
    package_scores.append(jsondata[package]['package_score'])
    for binary in jsondata[package]['binary_scores']:
        binary_scores.append(jsondata[package]['binary_scores'][binary])

p = sorted(package_scores)
b = sorted(binary_scores)

by_package = '' + \
            'Fedora 27 CTL scores by package:\n' + \
            '  n: ' + str(len(p)) + '\n' + \
            '  max: ' + str(max(p)) + '\n' + \
            '  min: ' + str(min(p)) + '\n' + \
            '  mean: ' + str(np.mean(p)) + '\n' + \
            '  median: ' + str(np.median(p)) + '\n' + \
            '  stdev: ' + str(np.std(p))

by_binary = '' + \
            'Fedora 27 CTL scores by binary:\n' + \
            '  n: ' + str(len(b)) + '\n' + \
            '  max: ' + str(max(b)) + '\n' + \
            '  min: ' + str(min(b)) + '\n' + \
            '  mean: ' + str(np.mean(b)) + '\n' + \
            '  median: ' + str(np.median(b)) + '\n' + \
            '  stdev: ' + str(np.std(b))

print(by_package)
print(by_binary)

pfit = stats.norm.pdf(p, np.mean(p), np.std(p))
pl.plot(p, pfit, 'o')
pl.hist(p, normed=True)
pl.text(-134, 0.0125, by_package, fontsize=9)
pl.show()

# bfit = stats.norm.pdf(b, np.mean(b), np.std(b))
# pl.plot(b, bfit, 'o')
# pl.hist(b, normed=True)
# pl.show()

