# cyber-test-lab

This tool is currently being rewritten. For the old version, refer to the [legacy](legacy) directory.

## Components

* Kubernetes: the orchestration framework
* [mirror-monitor](mirror-monitor/mirror-monitor.yml): monitors Linux distribution mirror sites and copies them to GCS
* [mirror-crawler-dispatcher](mirror-crawler-dispatcher/mirror-crawler-dispatcher.yml): looks for mirror urls in files captured by the mirror-monitor and dispatches a mirror-crawler pod
* mirror-crawler:
  * crawl mirrors identified by the mirror monitor
  * create package indices and puts them in Pub/Sub
* package-crawler: crawls the mirrors retrieved by mirror-crawler and:
  * looks for new packages
  * looks for packages with unexpected hashes
  * puts the packages in GCS
* scanner-monitor: looks for new packages to scan and dispatches scanner pods
* Scanners:
  * elf-scanner: static analyzer for Linux ELF executables