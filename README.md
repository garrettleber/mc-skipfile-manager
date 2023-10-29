# mc-skipfile-manager

A process which will monitor Minecraft servers for `.skip-stop` files, referred to as skipfiles, and remove them when their related `timefile` designates so.

## Overview

This app accepts one environment variable `$MC_SERVERS_DIR` which species a directory containing subdirectories of Minecraft servers. A tree might look like this:

```
.
├── rad2
│   ├── data
│   │   └── rad2
│   └── docker-compose.yml
└── vanilla
    ├── data
    │   ├── creative
    │   ├── fabric
    │   ├── fabric-creative
    │   ├── mc-velocity-proxy
    │   └── vanilla
    └── docker-compose.yml
```

Directories within `data/` are where the actual server data is (`server.properties`, world directories, etc.). In this example, `vanilla` is a proxied velocity network. It is actually multiple Minecraft "servers" but is only exposed as one endpoint and players use in-game commands to switch between them.

In those server data directories are the skipfiles which this script cleans.

We use `timefile`s which contain an epoch timestamp indicating when a skipfile has expired to determine whether to clean. These timefiles are created by external processes, currently only [mc-manager-api](https://github.com/garrettleber/mc-manager-api). We keep one `timefile` per stack (in our example that would be rad2 and vanilla). `timefile`s are kept in a separate directory, currently `/data/${stack}/timefile`. `/data` is a mounted volume on the docker container, which is also mounted on [mc-manager-api](https://github.com/garrettleber/mc-manager-api).

## TODO

- Make the timefile_dir configurable
- Docker image CI/CD
- `docker-compose.yml` example

## Pesonal reference

I'm using these commands to manually build my image at the moment:

```
docker build -t git.imkumpy.in/kumpy/mc-skipfile-manager:latest .
docker push git.imkumpy.in/kumpy/mc-skipfile-manager:latest
```

