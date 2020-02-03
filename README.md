# cyber-test-lab

This tool is currently being rewritten. For the old version, refer to the [legacy](legacy) directory.

## Components

* Kubernetes: the orchestration framework
* mirror-monitor: monitors Linux distribution mirror sites and copies them to GCS
* mirror-crawler: uses mirror files retrieved by the mirror-monitor to:
** crawl mirrors identified by the mirror monitor
** 
* package-monitor: montiors the mirrors for packages and retrieves them when they're new (or different)
* Scanners:
** elf-scanner: static analyzer for Linux ELF executables