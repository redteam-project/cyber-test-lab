#!/usr/bin/env python

import numpy as np
import scipy.stats as stats
import sys
import pylab as pl
import json

with open(sys.argv[1], 'r') as f:
    jsondata1 = json.load(f)
with open(sys.argv[2], 'r') as f:
    jsondata2 = json.load(f)

package_scores1 = []
binary_scores1 = []
for package in jsondata1.keys():
    package_scores1.append(jsondata1[package]['package_score'])
    for binary in jsondata1[package]['binary_scores']:
        binary_scores1.append(jsondata1[package]['binary_scores'][binary])

package_scores2 = []
binary_scores2 = []
for package in jsondata2.keys():
    package_scores2.append(jsondata2[package]['package_score'])
    for binary in jsondata2[package]['binary_scores']:
        binary_scores2.append(jsondata2[package]['binary_scores'][binary])

p1 = sorted(package_scores1)
b1 = sorted(binary_scores1)

p2 = sorted(package_scores2)
b2 = sorted(binary_scores2)

pfit1 = stats.norm.pdf(p1, np.mean(p1), np.std(p1))
pfit2 = stats.norm.pdf(p2, np.mean(p2), np.std(p2))

bfit1 = stats.norm.pdf(b1, np.mean(b1), np.std(b1))
bfit2 = stats.norm.pdf(b2, np.mean(b2), np.std(b2))

pl.figure(figsize=(15,5), dpi=150)

pl.subplot(1, 2, 1)
pl.hist(p1, normed=True, range=(-100,100), color='cornflowerblue', label='Fedora 27')
pl.legend(loc='upper left')

pl.subplot(1, 2, 2)
pl.hist(p2, normed=True, range=(-100,100), color='crimson', label='RHEL 7')
pl.legend(loc='upper left')

pl.show()
