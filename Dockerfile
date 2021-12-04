FROM ubuntu:bionic
LABEL maintainer "Delimbetov Kirill <1starfall1@gmail.com>"

# use bash so commands like source work
SHELL ["/bin/bash", "-c"]

# prepare directoar
ENV PROJECT_DIR=/project
ENV TMP_DIR=$PROJECT_DIR/tmp
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# get deps
## pillow deps
RUN apt-get update && apt-get install -y \
    libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev libopenjp2-7-dev

## python
RUN apt-get update && apt-get install -y \
    python3.7 \
    python3.7-dev \
    python3.7-venv \
    python3.7-distutils 

## other deps
RUN apt-get install -y curl

## pip
RUN mkdir -p $TMP_DIR
WORKDIR $TMP_DIR
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.7 get-pip.py
WORKDIR $PROJECT_DIR

# copy relevant data from build context
COPY ./ $PROJECT_DIR/

# init venv
RUN python3.7 -m venv venv
RUN source ./venv/bin/activate

# get pip deps
RUN pip3.7 install --upgrade pip
RUN pip3.7 install wheel setuptools
RUN pip3.7 install -r ./requirements.txt
RUN pip3.7 install Cython cymem preshed blis thinc
RUN pip3.7 install numpy

## no cache dir is to lower memory use
RUN pip3.7 install --no-cache-dir fastai

# Run
ENTRYPOINT ["python3.7", "main.py", "./data/export_resnet34_ft6.pkl"]
CMD ["api id", "api hash", "bot token"]

