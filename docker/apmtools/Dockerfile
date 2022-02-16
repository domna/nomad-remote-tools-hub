FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

# Needed to be set to run conda in the Dockerfile
ENV PATH=/usr/local/miniconda3/bin:$PATH

RUN apt-get update && lsb_release -a && apt-get install git:amd64=1:2.25.1-1ubuntu3 -y && git --version \
  && curl https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh --output miniconda3-install.sh \
  && chmod +x miniconda3-install.sh && bash ./miniconda3-install.sh -b -p /usr/local/miniconda3 \
  && conda install jupyter nomkl numpy matplotlib pandas \
  && conda install -c conda-forge jupyterlab \
  && mkdir -p /config/atom_probe_tools/leoben_apt_analyzer

#tkinter math struct already included in python3 by default

WORKDIR /config
RUN apt-get install unzip:amd64=6.0-25ubuntu1 -y \
  && curl --output APM.LEAP.Datasets.4.zip https://zenodo.org/record/6104015/files/APM.LEAP.Datasets.4.zip \
  && unzip APM.LEAP.Datasets.4.zip \
  && mkdir /config/atom_probe_tools \
  && mkdir /config/atom_probe_tools/leoben_apt_analyzer \
  && rm APM.LEAP.Datasets.4.zip \
  && mv 70_50_50.POS /config/atom_probe_tools/leoben_apt_analyzer/ \
  && mv AB.RRNG /config/atom_probe_tools/leoben_apt_analyzer/

COPY ["*.ipynb", "*.py", "*.pdf", "/config/atom_probe_tools/leoben_apt_analyzer/"]

RUN chown -R ${PUID}:${PGID} /config/atom_probe_tools && chown -R ${PUID}:${PGID} /usr/local/miniconda3

COPY 02-exec-cmd /config/custom-cont-init.d/02-exec-cmd
