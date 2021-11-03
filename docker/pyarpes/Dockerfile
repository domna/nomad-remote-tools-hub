FROM linuxserver/webtop:amd64-ubuntu-openbox-version-e1079163

RUN apt update \
    && apt install git:amd64=1:2.25.1-1ubuntu3 -y

# Helps install miniconda in the directory we have ownership over
ENV HOME=/pyarpes
# Install Miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh --output miniconda-install.sh \
    && chmod +x miniconda-install.sh \
    && bash ./miniconda-install.sh -b

# Needed to be set to run conda in the Dockerfile
ENV PATH=/pyarpes/miniconda3/bin:$PATH

RUN git clone https://github.com/Tommaso-Pincelli/arpes /pyarpes/arpes
WORKDIR /pyarpes/arpes
RUN git checkout 792a26dc0f335e2e310968d59750311b91209218

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "--no-capture-output", "-n", "arpes", "/bin/bash", "-c"]

RUN pip install .

RUN conda install -c conda-forge jupyterlab

COPY 01-chown-dir /config/custom-cont-init.d/01-chown-dir
COPY 02-exec-cmd /config/custom-cont-init.d/02-exec-cmd
COPY pyARPES_download_and_visualize.ipynb /pyarpes/example/pyARPES_download_and_visualize.ipynb
WORKDIR /pyarpes/example