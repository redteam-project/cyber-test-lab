# cyber-test-lab
Fedora Cyber Test Lab offers quantitative static and dynamic risk analysis of binaries

## Use

```python
# dnf install -y ansible yum
# ansible-playbook prep_fedora_host.yml
# virtualenv cyber-test-lab
# source cyber-test-lab/bin/activate
# pip install redteam

from cybertestlab import CyberTestLab
```