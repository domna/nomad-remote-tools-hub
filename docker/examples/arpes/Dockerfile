FROM linuxserver/webtop:ubuntu-openbox
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install git -y

# Install and configure miniconda
RUN git --version && wget --version

RUN mkdir -p /pyarpes/v3/thirdparty
WORKDIR /pyarpes/v3/thirdparty
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -O /pyarpes/v3/thirdparty/miniconda.sh
RUN chmod +x miniconda.sh
RUN bash ./miniconda.sh -b -p /pyarpes/v3/thirdparty/miniconda
ENV PATH=/pyarpes/v3/thirdparty/miniconda/bin:${PATH}
RUN lsb_release -a

## Needed to be set to run conda in the Dockerfile
##ENV PATH=/usr/local/miniconda/bin:$PATH
##RUN conda install -c nion nionswift nionswift-tool

## Add the command to run an app on startup
##RUN echo "/usr/local/miniconda/bin/nionswift" > /defaults/autostart

## Limit/Modify the application menu (right click desktop) for the user
##COPY menu.xml /defaults/menu.xml

# Get pyARPES source code
WORKDIR /pyarpes/v3
RUN git clone https://github.com/chstan/arpes.git
#unless further specified, will take the master branch which was when tested this between Oct 18 and Oct 28 the following, comment in the next line to checkout that specific commit
#RUN git checkout d982e4e6ce738fe757ee269af5e07925bbb237b3
RUN mv arpes python-arpes
WORKDIR python-arpes
RUN conda init bash
RUN conda env list
RUN conda env create -f environment.yml
RUN conda env list

#remain in base
RUN conda config --append channels conda-forge
RUN conda install -c arpes arpes
RUN conda install -c conda-forge jupyterlab
RUN mkdir -p research
#COPY tommasso_qt_test.py research
COPY Test.ipynb research
COPY FireUpPyArpes.bash /config
#.
WORKDIR /config
RUN chmod +x FireUpPyArpes.bash 
RUN whoami

#RUN groupadd -g 1001 arpesuser && useradd -r -u 1001 -g arpesuser arpi
#RUN chown arpi FireUp
#RUN chown -cR arpi research

