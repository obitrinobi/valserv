ARG CARLA_VERSION='0.9.9'
ARG CARLA_BUILD=''
ARG PYTHON_VERSION='3.6'

FROM ubuntu:18.04 as pythonrepo
FROM carlasim/carla:$CARLA_VERSION$CARLA_BUILD as carlarepo
FROM localhost:5000/airflow2:latest as airflowrepo

from pythonrepo
ENV DEBIAN_FRONTEND=noninteractive
ENV http_proxy "http://proxy-mu.intel.com:911"
ENV https_proxy "http://proxy-mu.intel.com:912"
RUN apt-get update && apt-get install -y --no-install-recommends \
    python \
    python-pip \
    python-dev \
    python3 \
    python3-pip \
    python3-dev \
    python3-wheel \
    build-essential \
    cmake \
    ninja-build \
    git \
#    clang++ \
    clang-8 \
    lld-8 \
    g++-7 \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libxerces-c-dev \
    unzip \
    tar \
    wget \
    rsync

RUN update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-8/bin/clang++ 180
RUN update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-8/bin/clang 180
#RUN ln -s /usr/bin/python3 /usr/bin/python && \
#    ln -s /usr/bin/pip3 /usr/bin/pip

ADD src /carla-service/src
ADD requirements.txt /carla-service
ADD setup.py /carla-service



WORKDIR ${HOME}/carla-service
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install setuptools
RUN pip install -r requirements.txt
RUN pip install .


COPY --from=carlarepo /home/carla/PythonAPI /carla/PythonAPI



ARG CARLA_VERSION

RUN mkdir carla-git
WORKDIR carla-git
RUN pip install distro
RUN git clone -b $CARLA_VERSION https://github.com/carla-simulator/carla.git .
RUN make PythonAPI.3
WORKDIR PythonAPI/carla
RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 7000
CMD ["python", "/carla-service/src/carla-service/api/service_main.py"]

