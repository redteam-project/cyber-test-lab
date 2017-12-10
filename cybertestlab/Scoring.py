#!/usr/bin/env python

import os
import sys
import json
import yaml

__author__ = 'Jason Callaway'
__email__ = 'jasoncallaway@fedoraproject.org'
__license__ = 'GNU Public License v2'
__version__ = '0.2'
__status__ = 'alpha'


class Analysis(object):
    def __init__(self, debug=False, schema='./scoring.yml'):
        self.debug = debug
        self.score_schema = schema
    
    def score(self, **kwargs):
        if kwargs.get('filename'):
            return {kwargs['filename']: self.score_json(kwargs['filename'])}
        if kwargs.get('path'):
            scores = {}
            for root, dirs, files in os.walk(kwargs['path']):
                for filename in files:
                    scores[filename] = score_json(filename)
            return scores 

    def score_json(self, filename):
        with open(filename, 'r') as f:
            jsondata = json.load(f)
         


