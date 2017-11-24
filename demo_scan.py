#!/usr/bin/env python

from cybertestlab import Analysis
import json
import sys
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

if len(sys.argv) > 1:
    a = Analysis.Analysis(sys.argv[1], debug=True)
else:
    a = Analysis.Analysis('/usr/bin', debug=True)

elfs = a.find_elfs()
b = a.scan_elfs(elfs)

for i in b.keys():
    try:
        es.update(id=i, index="ctl", doc_type='doc', body={'doc' :b[i], 'doc_as_upsert': True})
    except:
        # We'll figure this out someday
        pass

