import pytest

from cybertestlab import Analysis

def test_find_elfs():
    a = Analysis.Analysis('/usr/bin')

    elfs = a.find_elfs()
    assert len(elfs) > 0

def test_scan_elfs():
    a = Analysis.Analysis('/usr/bin')

    elfs = a.find_elfs()
    elfs = [elfs[1]]
    b = a.scan_elfs(elfs)
    assert b.has_key('complexity')
