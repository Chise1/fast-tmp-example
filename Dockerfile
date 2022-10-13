FROM python:3.8-slim
MAINTAINER Chise
RUN mkdir -p /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt -i https://pypi.python.org/simple
#RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./fast_tmp_example /src
COPY run.sh /src/
RUN chmod 777 run.sh
CMD ["./run.sh"]