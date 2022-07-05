FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

RUN apt update
RUN apt install git pip qt5-default python3-pyqt5 pyqt5-dev-tools cargo -y

RUN pip install --upgrade nodejs
RUN pip install ipywidgets h5glance==0.7 h5grove==0.0.14 \
    jupyterlab[full]==3.2.9 jupyterlab_h5web[full]==1.3.0 \
    punx==0.2.5 nexpy==0.14.1 silx[full]==1.0.0 --prefer-binary
RUN jupyter lab build
RUN jupyter nbextension enable --py widgetsnbextension
RUN jupyter serverextension enable jupyterlab_h5web

WORKDIR /
# Install nexus parser (w/o submodules, definitions are cloned seperately)
RUN git clone --recurse-submodules https://github.com/nomad-coe/nomad-parser-nexus.git 
WORKDIR /nomad-parser-nexus
RUN pip install -e . 

WORKDIR /
# Check out nexus definitions and set path
RUN git clone https://github.com/FAIRmat-Experimental/nexus_definitions
ENV NEXUS_DEF_PATH /nexus_definitions

RUN pip install git+https://github.com/rettigl/mpes@metadata
RUN pip install git+https://github.com/FAIRmat-Experimental/arpes.git

COPY 02-exec-cmd /config/custom-cont-init.d/02-exec-cmd
WORKDIR /config