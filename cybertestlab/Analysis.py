#!/usr/bin/env python

import os
import sys
import subprocess
import magic

import r2pipe

__author__ = 'Jason Callaway'
__email__ = 'jasoncallaway@fedoraproject.org'
__license__ = 'GNU Public License v2'
__version__ = '0.3'
__status__ = 'beta'


class Analysis(object):
    def __init__(self, path=None, debug=False):

        self.debug = debug
        self.path = path
        self.hardening_check = '/usr/bin/hardening-check'

    def find_elfs(self, **kwargs):
        path = self.path
        if kwargs.get('path'):
            path = kwargs['path']

        find_results = []

        rootDir = path
        for dirName, subdirList, fileList in os.walk(path):
            for fname in fileList:
                the_file = os.path.join(path, fname)
                try:
                    file_type = magic.from_file(the_file)
                    if 'ELF' in file_type:
                        find_results.append(the_file)
                except:
                    # Sometimes we fail to read the file for various
                    # reasons
                    pass

        elfs = []
        for result in filter(None, find_results):
            elfs.append(result.split(':')[0])

        if len(elfs) == 0:
            return None
        else:
            return filter(None, elfs)

    def scan_elfs(self, elfs):
        if not elfs:
            raise Exception('scan_elfs: you gave me an empty list of elfs you dope')
        scan_results = {}

        for elf in elfs:
            if self.debug:
                print('++ elf: ' + elf.replace(self.path + '/', ''))
            binary = elf
            relative_binary = \
                binary.replace(self.path + '/', '').replace('.', '_')

            scan_results[relative_binary] = {}
            scan_results[relative_binary]['filename'] = binary.replace(
                self.path + '/', '')

            # get hardening-check results
            cmd = self.hardening_check + ' ' + binary
            hardening_results = \
                self.run_command(cmd)

            # turn the hardening-check results into a dict
            pretty_results = {}
            for hr in hardening_results.split('\n'):
                if self.path in hr:
                    continue
                if hr == '':
                    continue
                hrlist = hr.split(':')
                test = hrlist[0]
                finding = hrlist[1]
                pretty_results[test.rstrip()] = finding.rstrip().lstrip()
            scan_results[relative_binary]['hardening-check'] = pretty_results

            # get function report
            cmd = self.hardening_check + ' -R ' + binary
            hardening_results = \
                self.run_command(cmd)
            # relevant stuff starts at 9th line
            scan_results[relative_binary]['report-functions'] = \
                filter(None, hardening_results.split('\n')[8:])

            # get libc functions
            cmd = self.hardening_check + ' -F ' + binary
            hcdashf = filter(
                None,
                self.run_command(cmd).split('\n')
            )
            hcdashf_clean = []
            for lib in hcdashf:
                if len(lib.split("'")) > 1:
                    hcdashf_clean.append(lib.split("'")[1])
                    scan_results[relative_binary]['find-libc-functions'] = \
                        hcdashf_clean
                else:
                    if self.debug:
                        print('+++ ' + elf.replace(self.path + '/', '') +
                              ' had no `hardening-check -F` output')

            scan_results[relative_binary]['complexity'] = self.get_complexity(binary)

        return scan_results

    def get_complexity(self, elf):
        if self.debug:
            print('++ get_complexity getting cyclomatic complexity via r2 for: ' + elf)
        complexity = 0
        cycles_cost = 0
        try:
            r2 = r2pipe.open(elf)
            if self.debug:
                print('++ starting aa')
            r2.cmd("aa")
            if elf.endswith('.so'):
                functions = r2.cmdj('afl')
                entry = 'entry'
                for f in functions:
                    if f.get('name'):
                        if f['name'] == 'entry0':
                            entry = 'entry0'
                cycles_cost = r2.cmdj('afC @' + entry)
                complexity = r2.cmdj('afCc @' + entry)
            elif elf.endswith('.a'):
                complexity = r2.cmdj('afCc')
            else:
                cycles_cost = r2.cmdj('afC @main')
                complexity = r2.cmdj('afCc @main')
        except Exception as e:
            if self.debug:
                print('+ get_complexity caught exception: ' + str(e))
            r2.quit()
            return {'r2aa': 'failed: ' + str(e)}

        r2.quit()
        return {'r2aa':
                    {'afCc': complexity,
                     'afC': cycles_cost
                     }
                }

    def run_command(self, cmd):
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            results = p.communicate()[0]
        except Exception as e:
            raise Exception(cmd + ' failed: ' + str(e))
        return results
