FROM jupyter/scipy-notebook

ENV HOME=/home/jovyan
WORKDIR $HOME

RUN git clone https://github.com/PyEllips/pyElli.git
WORKDIR ${HOME}/pyElli
RUN git checkout nexus-reader
RUN pip install -r requirements.txt
RUN pip install .

WORKDIR $HOME
RUN rm -rf pyElli
