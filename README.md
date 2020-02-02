# cyber-test-lab

This tool is currently being rewritten. For the old version, refer to the [legacy](legacy) directory.

## Components

* Kubernetes: the orchestration framework
* mirror-monitor: monitors Linux distribution mirrors and checks their integrity
* package-monitor: montiors the mirrors for packages and retrieves them when they're new (or different)
* Scanners:
** elf-scanner: static analyzer for Linux ELF executables