This is a Hello World/test image that includes a simple web-service with OAuth
authentication that authorizes against jupyterhub.

To build:
```
docker build -t north/oauth .
```

To use it, you have to adopt `/nomad/jupyterhub_config.py` (on the
[nomad-fair](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR) project) to use the
`north/oauth` as an image.