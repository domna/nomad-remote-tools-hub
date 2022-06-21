FROM jupyter/scipy-notebook

ENV HOME=/home/jovyan
WORKDIR $HOME

# Install packages and setup jupyter extensions
RUN pip install --upgrade nodejs
RUN pip install ipywidgets h5glance==0.7 h5grove==0.0.14 \
    jupyterlab[full]==3.2.9 jupyterlab_h5web[full]==1.3.0 punx==0.2.5 
RUN jupyter lab build
RUN jupyter nbextension enable --py widgetsnbextension
RUN jupyter serverextension enable jupyterlab_h5web

# Install nexus parser (w/o submodules, definitions are cloned seperately)
RUN git clone https://github.com/nomad-coe/nomad-parser-nexus.git
WORKDIR $HOME/nomad-parser-nexus
RUN git checkout mpes-latest
RUN pip install -e . 

# Check out nexus definitions
WORKDIR $HOME
RUN git clone https://github.com/FAIRmat-Experimental/nexus_definitions
WORKDIR $HOME/nexus_definitions
RUN git checkout fairmat

# Set the nexus definitions for the nexus parser
ENV NEXUS_DEF_PATH $HOME/nexus_definitions

# Copy files into homedir
WORKDIR $HOME/work
ADD --chown=${NB_UID}:${NB_GID} example $HOME/work