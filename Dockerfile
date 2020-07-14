FROM jupyter/base-notebook

USER root
WORKDIR /home

COPY  ./ta-lib-0.4.0-src.tar.gz /home/

RUN apt-get update
RUN apt-get --yes install build-essential
RUN tar -xzf ta-lib-0.4.0-src.tar.gz 
RUN cd ta-lib &&\
    ./configure --prefix=/usr  &&\
    make &&\
    make install 

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  pandas numpy tushare backtrader[plotting]  TA-Lib
