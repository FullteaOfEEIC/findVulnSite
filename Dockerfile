FROM ubuntu:18.04

LABEL author frt@frt.hongo.wide.ad.jp
ARG PYTHON_VERSION=3.9.1

RUN apt update && apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y\
 make\
 build-essential\
 libssl-dev\
 zlib1g-dev\
 libbz2-dev\
 libreadline-dev\
 libsqlite3-dev\
 wget\
 curl\
 llvm\
 libncurses5-dev\
 libncursesw5-dev\
 xz-utils\
 tk-dev\
 libffi-dev\
 liblzma-dev\
 git\
 nikto\
 dirb\
 nmap\
 firefox-geckodriver\
 sudo

RUN git clone https://github.com/pyenv/pyenv.git /.pyenv && sh /.pyenv/plugins/python-build/install.sh && rm -rf /.pyenv
RUN mkdir /python && /usr/local/bin/python-build -v ${PYTHON_VERSION} /python
ENV PATH $PATH:/python/bin
RUN pip install --upgrade pip setuptools

RUN pip install\
 python-nmap\
 jupyter\
 numpy\
 tqdm\
 requests\
 tqdm\
 selenium\
 python-docx\
 timeout_decorator

RUN git clone https://github.com/aboul3la/Sublist3r.git
RUN pip install -r Sublist3r/requirements.txt

ADD src /
ADD datasets /datasets
ADD assets /assets

ENTRYPOINT ["python", "main.py"]
CMD ["127.0.0.1"]