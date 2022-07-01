FROM jupyter/scipy-notebook

ENV HOME=/home/jovyan
WORKDIR $HOME

# Setup jupyterlab and NeXus tools
RUN pip install --upgrade nodejs
RUN pip install ipywidgets h5glance==0.7 h5grove==0.0.14 \
    jupyterlab[full]==3.2.9 jupyterlab_h5web[full]==1.3.0 punx==0.2.5 \
    plotly ipython
RUN jupyter lab build
RUN jupyter nbextension enable --py widgetsnbextension
RUN jupyter serverextension enable jupyterlab_h5web

# Install nexus parser (w/o submodules, definitions are cloned seperately)
RUN git clone https://github.com/nomad-coe/nomad-parser-nexus.git 
WORKDIR $HOME/nomad-parser-nexus
RUN pip install -e . 
WORKDIR $HOME

# Check out nexus definitions and set path
RUN git clone --branch fairmat-ellips https://github.com/FAIRmat-Experimental/nexus_definitions
ENV NEXUS_DEF_PATH $HOME/nexus_definitions

# Install pyElli ellipsometry analysis tool
RUN pip install pyElli