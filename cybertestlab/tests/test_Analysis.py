import pytest

from cybertestlab import Analysis

def test_find_elfs():
    a = Analysis.Analysis('/usr/bin')

    elfs = a.find_elfs()
    assert len(elfs) > 0

def test_scan_elfs():
    a = Analysis.Analysis('/usr/bin')

    b = a.scan_elfs(['/usr/bin/yes'])
    assert b.has_key('yes')

def test_get_complexity():

    a = Analysis.Analysis('/usr/bin')
    b = a.get_complexity('/usr/bin/yes')
    assert b.has_key('r2aa')
