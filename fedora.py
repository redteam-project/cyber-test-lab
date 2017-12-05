#!/usr/bin/env python

import json
import os
import sys
import traceback

from datetime import datetime

__author__ = 'Jason Callaway'
__email__ = 'jasoncallaway@fedoraproject.org'
__license__ = 'GNU Public License v2'
__version__ = '0.1'
__status__ = 'alpha'

sys.path.append('.')
from cybertestlab import CyberTestLab

debug = True
now = datetime.now()
# output_dir = './ctl-results/fedora/27'
# repo_dir = '/repo'
# swap_path = '/fedora_swap'
output_dir = sys.argv[0]
repo_dir = sys.argv[1]
swap_path = sys.argv[2]
repos = ['fedora']
ctl = CyberTestLab.CyberTestLab(repo_dir=repo_dir,
                                swap_path=swap_path,
                                repos=repos,
                                debug=True)
ctl.redteam.funcs.mkdir_p(repo_dir)
ctl.redteam.funcs.mkdir_p(swap_path)

# if debug:
#     print('+ syncing repos')
# ctl.repo_sync('reposync')

for repo in ctl.repo_list:
    for root, dirs, files in os.walk(repo_dir + '/' + repo):
        for filename in files:
            if debug:
                print('+ ' + filename)
            ctl.prep_swap()
            try:
                results_dir = output_dir + '/' + filename[0]
                results_file = results_dir + '/' + filename + '.json'
                if not os.path.isfile(results_file):
                    ctl.prep_rpm(repo, filename)
                    metadata = ctl.get_metadata(filename)
                    elfs = ctl.find_elfs()
                    if elfs:
                        results = ctl.scan_elfs(filename, elfs)
                        ctl.redteam.funcs.mkdir_p(results_dir)
                        with open(results_file, 'w') as f:
                            json.dump({'metadata': metadata,
                                       'results': results}, f, indent=4)
            except Exception as e:
                print('fedora analysis failed on ' + filename)
                traceback.print_exc()
                continue

1