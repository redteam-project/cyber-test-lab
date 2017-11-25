# cyber-test-lab
Fedora Cyber Test Lab offers quantitative static and dynamic risk analysis of binaries

## Super alpha-y
This barely works. And the data it produces is crap. You should probably just move along and come back later.

But hey, release early, release often.

## Use

If you really want to try and use this, you could do this...

```python
# dnf install -y ansible yum
# ansible-playbook prep_fedora_host.yml
# virtualenv cyber-test-lab
# source cyber-test-lab/bin/activate
# pip install redteam python-magic

from cybertestlab import CyberTestLab
```

Or just check out [fedora.py](https://github.com/fedoraredteam/cyber-test-lab/blob/master/fedora.py).

## Tests
You need to set PYTHONPATH to '.' then run py.test

## Storing results
You can use the demo_scan.py script to store the results of a scan in
elasticsearch. The Elasticsearch python module needs to be installed.

