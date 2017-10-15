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
output_dir = './ctl-results/fedora/26'
repo_dir = '/testrepo'
swap_path = '/fedora_swap'
repos = ['fedora']
ctl = CyberTestLab.CyberTestLab(repo_dir=repo_dir,
                                swap_path=swap_path,
                                repos=repos)
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
                ctl.prep_rpm(repo, filename)
                metadata = ctl.get_metadata(filename)
                elfs = ctl.find_elfs()
                if elfs:
                    if debug:
                        print('+ elfs: ' + ', '.join(elfs))
                    results = ctl.scan_elfs(filename, elfs)
                    results_dir = output_dir + '/' + filename[0]
                    ctl.redteam.funcs.mkdir_p(results_dir)
                    results_file = results_dir + '/' + filename + '.json'
                    with open(results_file, 'w') as f:
                        json.dump({'metadata': metadata,
                                   'results': results}, f, indent=4)
            except Exception as e:
                print('fedora analysis failed on ' + filename)
                traceback.print_exc()
                continue

1