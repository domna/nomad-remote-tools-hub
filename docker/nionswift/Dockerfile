FROM continuumio/miniconda3:4.7.12-alpine as builder

RUN /opt/conda/bin/conda install -c nion nionswift=0.15.7 nionswift-tool=0.4.13

USER root
RUN apk add --no-cache git && /opt/conda/bin/pip install git+https://git.physik.hu-berlin.de/kornilog/nionswift_frwr_plugin.git@4407db6b2d5e96be52f959f1cc84fc9861548b2f

FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/webtop

COPY --from=builder /opt/conda/bin /opt/conda/bin
COPY --from=builder /opt/conda/lib /opt/conda/lib

# Add the command to run an app on startup
RUN echo "/opt/conda/bin/nionswift" > /defaults/autostart

# Limit/Modify the application menu (right click desktop) for the user
COPY menu.xml /defaults/menu.xml