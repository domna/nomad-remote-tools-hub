FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

# Stack of major installs
RUN apt-get update && lsb_release -a && \
    apt-get install -y alien:amd64=8.95 \
        h5utils:amd64=1.13.1-3build1 \
        hdf-compass:amd64=0.7~b8-2 \
        hdf5-tools:amd64=1.10.4+repack-11ubuntu1 \
        libhdf5-openmpi-dev:amd64=1.10.4+repack-11ubuntu1 \
        wget:amd64=1.20.3-1ubuntu1 \
        git:amd64=1:2.25.1-1ubuntu3 \
        libhdf5-dev:amd64=1.10.4+repack-11ubuntu1 \
        cmake:amd64=3.16.3-1ubuntu1 \
        libxml2-dev:amd64=2.9.10+dfsg-5ubuntu0.20.04.1 && \
    wget https://support.hdfgroup.org/ftp/HDF5/releases/HDF-JAVA/hdfview-3.1.2/bin/HDFView-3.1.2-centos7_64.tar.gz && \
    tar xfvz HDFView-3.1.2-centos7_64.tar.gz && \
    alien --scripts hdfview-3.1.2-1.x86_64.rpm && \
    echo "ls" > myscript && chmod a+x myscript && \
    ln -s /myscript /bin/xdg-desktop-menu && \
    ln -s /myscript /bin/xdg-mime && \
    dpkg -i hdfview_3.1.2-2_amd64.deb && \
    chmod -R a+rX /opt/hdfview && \
    ln -s /opt/hdfview/bin/HDFView /bin/ && \
    apt-get install pip -y && \
    pip install h5py==3.5.0 \
        h5glance==0.7 \
        h5grove==0.0.8 \
        jupyterlab[full]==2.3.0 \
        jupyterlab_h5web[full]==0.0.11 \
        punx==0.2.5 \
        nexpy==0.14.1 \
        silx[full] && \
    jupyter lab build

#nexus definitions
RUN git clone https://github.com/nexusformat/definitions

#cnxvalidate
RUN git clone https://github.com/nexusformat/cnxvalidate
WORKDIR cnxvalidate
RUN mkdir build
WORKDIR build
RUN cmake ../ && \
    make && \
    ln -s /cnxvalidate/build/nxvalidate /bin/
WORKDIR /
#launch: nxvalidate -l /definitions/ <nexusfile>

#h5nuvola2
RUN git clone https://gitlab.elettra.eu/andrea.lorenzon/h5nuvola2
RUN pip install Flask==1.1.2
#modify settings.py
#export FLASK_APP=app.py
#launch: python3 -m flask run

#dials
#RUN wget https://dials.diamond.ac.uk/diamond_builds/dials-linux-x86_64-conda3.tar.xz
#RUN tar -xJf dials-linux-x86_64-conda3.tar.xz
#WORKDIR dials-installer-dev
#RUN ./install --prefix=/DIALS/
#launch: source /DIALS/dials-dev/dials_env.sh && dials.image_viewer
#WORKDIR /

#nexus-parser
RUN git clone https://github.com/nomad-coe/nomad-parser-nexus.git
#export NEXUS_DEF_PATH=/definitions/
#launch checker: python3 /nomad-parser-nexus/nexusparser/tools/read_nexus.py <nexusfile>
