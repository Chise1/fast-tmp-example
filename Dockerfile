FROM python:3.8-slim
MAINTAINER Chise
RUN mkdir -p /src
WORKDIR /src
ENV POETRY_VIRTUALENVS_CREATE=false
COPY run.sh /src/
RUN chmod 777 run.sh
RUN pip3 install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY pyproject.toml poetry.lock /src/
RUN poetry install --without dev
COPY ./fast_tmp_example /src
CMD ["./run.sh"]