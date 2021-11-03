FROM jupyter/datascience-notebook:ubuntu-20.04
RUN whoami
RUN echo $UID
USER root
RUN whoami
RUN echo $UID
RUN sudo apt-get update

#ENV TZ=Europe/Berlin
#RUN apt-get install tzdata -y
RUN apt-get install m4:amd64=1.4.18-4 -y
RUN apt-get install file:amd64=1:5.38-4 -y
RUN apt-get install vim:amd64=2:8.1.2269-1ubuntu5.3 -y
RUN apt-get install build-essential:amd64=12.8ubuntu1.1 -y
RUN gcc --version && g++ --version && make -v
RUN apt-get install mpich:amd64=3.3.2-2build1 -y
RUN mpiexec --version && apt-get clean

RUN apt-get install libgmp-dev:amd64=2:6.2.0+dfsg-4 -y
RUN apt-get install libmpfr-dev:amd64=4.0.2-1 -y

WORKDIR /home/jovyan/work
RUN mkdir -p /home/jovyan/work/paraprobe
WORKDIR paraprobe
RUN git clone https://gitlab.com/paraprobe/paraprobe-toolbox.git
WORKDIR paraprobe-toolbox
RUN git checkout 51b7f76df6b3297a546bc34e271c5cf4300b0c4d
WORKDIR code/thirdparty/mandatory

RUN mkdir -p cmake
WORKDIR cmake
RUN wget https://cmake.org/files/v3.19/cmake-3.19.4.tar.gz && tar -xvf cmake-3.19.4.tar.gz
WORKDIR cmake-3.19.4
RUN chmod +x bootstrap && ./bootstrap -- -DCMAKE_BUILD_TYPE=Release -DCMAKE_USE_OPENSSL=OFF && make -j8 && make install
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/cmake
RUN ls
RUN rm cmake-3.19.4.tar.gz && cmake --version
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

RUN mkdir -p hdf5
WORKDIR hdf5
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.1/src/CMake-hdf5-1.12.1.tar.gz
RUN gunzip CMake-hdf5-1.12.1.tar.gz && tar -xvf CMake-hdf5-1.12.1.tar
WORKDIR CMake-hdf5-1.12.1
RUN ./build-unix.sh && ./HDF5-1.12.1-Linux.sh --include-subdir --skip-license  
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/hdf5
RUN rm CMake-hdf5-1.12.1.tar
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

# no need to install special version of gmp and mpfr use the ones that were installed with apt-get above

WORKDIR tetgen
RUN tar -xvf tetgen1.6.0.tar.gz
WORKDIR tetgen1.6.0
RUN make -j8 tetlib
#add to path, but do not delete tetgen1.6.0.tar.gz #RUN rm tetgen1.6.0.tar.gz
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

RUN mkdir -p fftw
WORKDIR fftw
RUN wget https://www.fftw.org/fftw-3.3.10.tar.gz && tar -xvf fftw-3.3.10.tar.gz
WORKDIR fftw-3.3.10
RUN ./configure --enable-float --enable-sse && make -j8 && make check && make install
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/fftw
RUN rm fftw-3.3.10.tar.gz
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

WORKDIR voroxx
RUN tar -xvf voro++-0.4.6.tar.xz
RUN rm voro++-0.4.6.tar.xz
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

RUN mkdir -p boost
WORKDIR boost
RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/boost_1_77_0.tar.gz && tar -xvf boost_1_77_0.tar.gz
WORKDIR boost_1_77_0
ENV PATH="/home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/boost/boost_1_77_0/:${PATH}"
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/boost
RUN rm boost_1_77_0.tar.gz
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

RUN mkdir -p eigen
WORKDIR eigen
RUN wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz && tar -xvf eigen-3.4.0.tar.gz
WORKDIR eigen-3.4.0
ENV PATH="/home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/eigen/eigen-3.4.0/:${PATH}"
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/eigen
RUN rm eigen-3.4.0.tar.gz
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

RUN mkdir -p cgal
WORKDIR cgal
RUN wget https://github.com/CGAL/cgal/releases/download/v5.3/CGAL-5.3.tar.xz && tar -xvf CGAL-5.3.tar.xz
#remove maybe the examples to reduce the size of the image
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/cgal
#RUN rm -ŕf CGAL-5.3/examples/ && rm CGAL-5.3.tar.xz
#WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory

# finally source code files and headers for Lewiner2002, Hornus2017, hdf5cxx wrapper are already there from git clone
# because its part of the gitlab repo, with this the installation and configuration of prerequisities is complete
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# now compile the paraprobe tools from their source code portions
# paraprobe-utils tool, copy source code in there, replace later a pull from the GitLab repo of the docker branch
RUN mkdir -p paraprobe-utils/build
WORKDIR paraprobe-utils/build
RUN cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=mpicxx .. && make -j8
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# paraprobe-ranger tool
RUN mkdir -p paraprobe-ranger/build
WORKDIR paraprobe-ranger/build
RUN cmake -DMYGITSHA=0 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=mpicxx .. && make -j8
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# paraprobe-surfacer tool
RUN mkdir -p paraprobe-surfacer/build
WORKDIR paraprobe-surfacer/build
RUN cmake -DBOOST_ROOT=/home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/boost/boost_1_77_0 -DEIGEN3_INCLUDE_DIR=/home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/eigen/eigen-3.4.0 -DCGAL_DIR=/home/jovyan/work/paraprobe/paraprobe-toolbox/code/thirdparty/mandatory/cgal/CGAL-5.3 -DMYGITSHA=0 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=mpicxx .. && make -j8
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# paraprobe-distancer tool
RUN mkdir -p paraprobe-distancer/build
WORKDIR paraprobe-distancer/build
RUN cmake -DMYGITSHA=0 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=mpicxx .. && make -j8
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# paraprobe-tessellator tool
RUN mkdir -p paraprobe-tessellator/build
WORKDIR paraprobe-tessellator/build
RUN cmake -DMYGITSHA=0 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=mpicxx .. && make -j8
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox/code

# examples were already copied from the repository now move them in a place that resolve from which APTFIM group they come
WORKDIR /home/jovyan/work/paraprobe/paraprobe-toolbox
RUN mkdir -p research/database/usa_portland_wang
RUN mv research/PARAPROBE.Transcoder.Results.SimID.0.zip research/database/usa_portland_wang
#the example we want to offer users to get started
RUN mv research/PARAPROBE.NomadNorthToolExample.SimID.0.ipynb /home/jovyan

#we are still root but when running the container we are jovyan so we need to make the research folder accessible
#take only ownership of example data
RUN chown -cR jovyan /home/jovyan/work/paraprobe/paraprobe-toolbox/research/database/usa_portland_wang
#the container will startup from ~joyvan though, so we should have a softlink pointing to the above example files
WORKDIR /home/jovyan
RUN ln -s /home/jovyan/work/paraprobe/paraprobe-toolbox/research/database/usa_portland_wang/PARAPROBE.Transcoder.Results.SimID.0.zip PARAPROBE.Transcoder.Results.SimID.0.zip
RUN chown -c jovyan /home/jovyan/PARAPROBE.Transcoder.Results.SimID.0.zip
RUN chown -c jovyan /home/jovyan/PARAPROBE.NomadNorthToolExample.SimID.0.ipynb

RUN ln -s /home/jovyan/work/paraprobe/paraprobe-toolbox/code/paraprobe-ranger/build/paraprobe_ranger /bin/ && \
ln -s /home/jovyan/work/paraprobe/paraprobe-toolbox/code/paraprobe-surfacer/build/paraprobe_surfacer /bin/ && \
ln -s /home/jovyan/work/paraprobe/paraprobe-toolbox/code/paraprobe-distancer/build/paraprobe_distancer /bin/ && \
ln -s /home/jovyan/work/paraprobe/paraprobe-toolbox/code/paraprobe-tessellator/build/paraprobe_tessellator /bin/ 
#WORKDIR /home/jovyan

#finally change to user jovyan
USER 1000

#and display how final rights are in the container
RUN pwd && ls -lah
