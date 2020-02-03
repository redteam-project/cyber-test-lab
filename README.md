# cyber-test-lab

This tool is currently being rewritten. For the old version, refer to the [legacy](legacy) directory.

## Components

* Kubernetes: the orchestration framework
* [mirror-monitor](mirror-monitor/mirror-monitor.yml): monitors Linux distribution mirror sites and copies them to GCS
* mirror-crawler: uses mirror files retrieved by the mirror-monitor to:
** crawl mirrors identified by the mirror monitor
** create package indices and put them in GCS
* package-crawler: crawls the mirrors retrieved by mirror-crawler and:
** looks for new packages
** looks for packages with unexpected hashes
** puts the packages in GCS
* package-monitor: looks for recently updated packages to scan
* Scanners:
** elf-scanner: static analyzer for Linux ELF executables