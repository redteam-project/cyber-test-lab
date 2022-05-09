# cyber-test-lab

**Note that as of May 2022 this project is no longer active.**

Cyber Test Lab offers quantitative static and dynamic risk analysis of binaries

This project is in beta. It can still be hard to get working. Contact [jasoncallaway@google.com](matilto:jasoncallaway@google.com) for help.

If you're looking for a place to contribute, we need help with documentation! For development contributions, read on.

## Warning - this is broken
We're still in the process of migrating this tool from the [old project](https://github.com/fedoraredteam/cyber-test-lab), but we're actively working on fixing it. Check back soon for updates.

## How to run CTL

The CTL code can be executed from within a docker container, making cross-platform development much easier. These instructions assume [PyCharm](https://www.jetbrains.com/pycharm/) is your development environment, but others will work fine too.

First, set up [PyCharm](https://www.jetbrains.com/pycharm/download/#section=linux) and [Docker](https://docs.docker.com/get-started/) on your system.

Next, configure PyCharm's Docker plugin. Here's a [tutorial](https://blog.jetbrains.com/pycharm/2015/12/using-docker-in-pycharm/).

Now it's time to build your CTL container.

```bash
git clone https://github.com/redteam-project/cyber-test-lab
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
