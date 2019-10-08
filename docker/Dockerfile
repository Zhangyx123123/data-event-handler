FROM python:3.6.7

ENV TZ=Asia/Shanghai

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt
RUN pip install gevent
ENV PYTHONPATH /usr/src/app

COPY . /usr/src/app

WORKDIR "/usr/src/app"
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
