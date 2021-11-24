FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

RUN apt update \
    && apt install git:amd64=1:2.25.1-1ubuntu3 -y \
    && export HOME=/pyarpes \
    && curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh --output miniconda-install.sh \
    && chmod +x miniconda-install.sh \
    && bash ./miniconda-install.sh -b \
    && chown -R ${PUID}:${PGID} /pyarpes/miniconda3/bin \
    && export PATH=/pyarpes/miniconda3/bin:$PATH \
    && git clone https://github.com/Tommaso-Pincelli/arpes /pyarpes/arpes \
    && cd /pyarpes/arpes \
    && git checkout be27050716f9e306b99f6e6b416f82bfb071c8b4 \
    && conda env create -f environment.yml \
    && conda run --no-capture-output -n arpes pip install . \
    && conda run --no-capture-output -n arpes conda install -c conda-forge jupyterlab \
    && chown -R ${PUID}:${PGID} /pyarpes

COPY 02-exec-cmd /config/custom-cont-init.d/02-exec-cmd
