# Local install

This readme guides you through the process of setting up the example pipeline for mpes locally on your working machine. There are two methods available, one is to use a pre-built docker container with all packages installed and the second method is installing the python packages in the local python version. The docker install is easier and recommended.

## Docker

### Setup of docker and docker-compose

If you already have a running docker and docker-compose on your local system you can skip this section.
To setup your local docker on a workstation we recommand using docker desktop, which is a program to provide docker functionality on desktop machines. Please follow their [install instructions](https://docs.docker.com/desktop/#download-and-install). Additionally, you need to install [docker-compose](https://docs.docker.com/compose/install/compose-desktop/).

### Running of mpes examples

Please make sure your docker desktop is up and running.
To run the provided examples you just have to execute the command
`docker-compose up`
in the example directory.
This will spin up the docker containers for you and you should be able to access the jupyter hub by clicking on the link at the end of the docker output.

## Bare-metal install
It is recommended to use a python virtualenv for the installation of the packages so you keep it seperated from your other packages as some of the procedures install specific version of packages. [Here](https://janakiev.com/blog/jupyter-virtual-envs/) is a guide on how to setup a virtualenv and how to make it available in jupyter.

First the jupyter and required jupyter packages are installed.
```
pip install --upgrade nodejs
pip install ipywidgets h5glance==0.7 h5grove==0.0.14 \
 jupyterlab[full]==3.2.9 jupyterlab_h5web[full]==1.3.0 punx==0.2.5
 ```

In the next step jupyter and its extensions are rebuild.
```
jupyter lab build
jupyter nbextension enable --py widgetsnbextension
jupyter serverextension enable jupyterlab_h5web
```

Now, we are ready to install the mpes related packages.
First, we need the [mpes package](https://github.com/rettigl/mpes) which provides distributed data processing routines for mpes.
`pip install git+https://github.com/rettigl/mpes.git@metadata`

The next package is the [nomad-parser](https://github.com/nomad-coe/nomad-parser-nexus), which provides reading and writing capabilities for the MPES NeXus files.
`pip install git+https://github.com/nomad-coe/nomad-parser-nexus.git`

For analysis and visualization we additionally install the [pyArpes package](https://github.com/FAIRmat-Experimental/arpes.git)
`pip install git+https://github.com/FAIRmat-Experimental/arpes.git`

Now you should be able to start the example notebooks with jupyter lab. To start the jupyter server just execute the command
`jupyter lab`
in the example directory.
