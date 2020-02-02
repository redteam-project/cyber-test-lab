#!/usr/bin/env python

import sys
import json

sys.path.append('.')
from cybertestlab import Scoring

__author__ = 'Jason Callaway'
__email__ = 'jasoncallaway@fedoraproject.org'
__license__ = 'GNU Public License v2'
__version__ = '0.3'
__status__ = 'beta'


def main(argv):
    s = Scoring.Scoring(debug=True)

    scores = s.score(path=sys.argv[1])

    with open(sys.argv[2], 'w') as f:
        json.dump(scores, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    main(sys.argv)
