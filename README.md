# NOMAD remote tools hub (north)

Lets you run containarized tools remotly.

North is based on Jupyterhub and NOMAD. NOMAD runs Jupyterhub as a separate service,
provides GUI elements that connect to Jupyterhub to launch and control North tools.
This project contains all necessary docker images with all the supported tools inside.

## Project structure

- `docker` - All the docker files, scripts for creating/managing images, documentation

## Getting started

Clone the project

```sh
git clone git@gitlab.mpcdf.mpg.de:nomad-lab/nomad-remote-tools-hub.git
cd nomad-remote-tools-hub
```

Get all sub-modules

```sh
git submodule update --init
```

Build an image
```sh
cd docker/webtop
docker build -t gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop .
```

See the respective `README.md` of `docker/*` subdirectories.
