FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

# Install Miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh --output miniconda-install.sh \
    && chmod +x miniconda-install.sh \
    && bash ./miniconda-install.sh -b -p /usr/local/miniconda

# Needed to be set to run conda in the Dockerfile
ENV PATH=/usr/local/miniconda/bin:$PATH
RUN conda install -c nion nionswift=0.15.7 nionswift-tool=0.4.13

# Add the command to run an app on startup
RUN echo "/usr/local/miniconda/bin/nionswift" > /defaults/autostart

# Limit/Modify the application menu (right click desktop) for the user
COPY menu.xml /defaults/menu.xml