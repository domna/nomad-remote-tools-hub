FROM linuxserver/webtop:amd64-ubuntu-openbox-version-e1079163
RUN apt-get update && lsb_release -a
RUN apt-get install wget:amd64=1.20.3-1ubuntu1 -y
RUN apt-get install git:amd64=1:2.25.1-1ubuntu3 -y
RUN git --version && wget --version

RUN mkdir -p /pyarpes/v3/thirdparty
WORKDIR /pyarpes/v3/thirdparty
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -O /pyarpes/v3/thirdparty/miniconda.sh
RUN chmod +x miniconda.sh
RUN bash ./miniconda.sh -b -p /pyarpes/v3/thirdparty/miniconda
ENV PATH=/pyarpes/v3/thirdparty/miniconda/bin:${PATH}

WORKDIR /pyarpes/v3
#RUN git clone https://github.com/chstan/arpes.git
RUN git clone https://github.com/Tommaso-Pincelli/arpes
RUN mv arpes python-arpes
WORKDIR python-arpes
#RUN git checkout d982e4e6ce738fe757ee269af5e07925bbb237b3
RUN git checkout 792a26dc0f335e2e310968d59750311b91209218

RUN conda init bash
RUN conda env list && conda env create -f environment.yml && conda env list
RUN conda config --append channels conda-forge
RUN conda install -c arpes arpes
RUN conda install -c conda-forge jupyterlab
RUN mkdir -p research
#COPY PyArpesWithQtInNorthUbuntuWebTop.ipynb research
#RUN echo "/usr/local/miniconda/bin/jupyter-notebook" > /defaults/autostart

#COPY FireUpPyArpes.bash /config
#WORKDIR /config
#RUN chmod +x FireUpPyArpes.bash 
#RUN whoami


