# cyber-test-lab
Fedora Cyber Test Lab offers quantitative static and dynamic risk analysis of binaries

## Alpha
This project is in alpha. It can be hard to get working. Contact [jasoncallaway@fedoraproject.org](matilto:jasoncallaway@fedoraproject.org) for help.

We're targeting end of December 2017 for a beta release.

## How to contribute

The CTL code can be executed from within a docker container, making cross-platform development much easier. These instructions assume [PyCharm](https://www.jetbrains.com/pycharm/) is your development environment, but others will work fine too.

<<<<<<< HEAD
First, set up [PyCharm](https://www.jetbrains.com/pycharm/download/#section=linux) and [Docker](https://docs.docker.com/get-started/) on your system.
=======
```python
# dnf install -y ansible yum
# ansible-playbook prep_fedora_host.yml
# virtualenv cyber-test-lab
# source cyber-test-lab/bin/activate
# pip install redteam python-magic
>>>>>>> 17a48fa513e46fbf37fa9b6161796a8d9f06b417

Next, configure PyCharm's Docker plugin. Here's a [tutorial](https://blog.jetbrains.com/pycharm/2015/12/using-docker-in-pycharm/).

Now it's time to build your CTL container.

```bash
git clone https://github.com/fedoraredteam/cyber-test-lab
cd cyber-test-lab/docker
docker built -t fctl .
```

Then you can configure your [remote interpreter](https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-docker.html) in PyCharm.

You've got one step left before you can run the CTL, which is downloading some packages. Since docker containers are ephemeral, you want to mount a local directory into the fctl container before syncing any repos.

On Docker 17.06 or later:
```bash
docker run --rm -ti \
  --mount type=bind,source="~/fctl/fedora27",target=/repo \
  fctl \
  timeout 600 reposync -p /repo
```

<<<<<<< HEAD
On earlier versions:
```bash
docker run --rm -ti -v /home/jason/fctl/fedora27:/repo fctl \
  timeout 600 reposync -p /repo
```

Note that if you're using Fedora, RHEL, or a variant, you'll need to add a ```:z``` to the bind mount for SELinux relabeling. I.E., ```-v /home/jason/fctl/fedora27:/repo:z```.

Now you should have some rpms with binaries to analyze. Note that we're using ```timeout``` to sync for 10 minutes to limit disk usage. Remove ```timeout 600``` if you want the whole shebang.

The last step is to create a new run/debug configuration. But there are two tricky parts:

1. Be sure to pick the remote docker interpreter under "Python Interpreter"
2. Mount the repo using Docker Container Image Settings > Volume Bindings. Be sure to use the same mapping as above, i.e., ```/home/jason/fctl/fedora27``` to ```/repo```.
=======
Or just check out [fedora.py](https://github.com/fedoraredteam/cyber-test-lab/blob/master/fedora.py).

## Tests
You need to set PYTHONPATH to '.' then run py.test

## Storing results
You can use the demo_scan.py script to store the results of a scan in
elasticsearch. The Elasticsearch python module needs to be installed.
>>>>>>> 17a48fa513e46fbf37fa9b6161796a8d9f06b417

