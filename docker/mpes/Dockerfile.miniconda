FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

RUN apt update
RUN apt install git:amd64=1:2.25.1-1ubuntu3 -y
ENV HOME /pyarpes
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh --output miniconda-install.sh 
RUN chmod +x miniconda-install.sh 
RUN bash ./miniconda-install.sh -b 
RUN chown -R ${PUID}:${PGID} /pyarpes/miniconda3/bin 
ENV PATH="/pyarpes/miniconda3/bin:{$PATH}"
RUN git clone https://github.com/Tommaso-Pincelli/arpes /pyarpes/arpes 
WORKDIR /pyarpes/arpes 
RUN git checkout be27050716f9e306b99f6e6b416f82bfb071c8b4 
RUN conda env create -f environment.yml 
RUN conda run --no-capture-output -n arpes pip install . 
RUN conda run --no-capture-output -n arpes conda install -c conda-forge jupyterlab 
RUN chown -R ${PUID}:${PGID} /pyarpes

COPY 02-exec-cmd /config/custom-cont-init.d/02-exec-cmd
