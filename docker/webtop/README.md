This is a customized webtop image that includes a modified gClient with OAuth
authentication that authorizes against jupyterhub.

To build:
```
docker build -t gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop .
```

To push:
```
docker login gitlab-registry.mpcdf.mpg.de
docker push gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop
```

To use it, you have to adopt `/nomad/jupyterhub_config.py` (on the
[nomad-fair](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR) project) to use the
`gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop` as an image.
