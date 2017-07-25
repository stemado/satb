
FROM python:3.5
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /requirements.txt
ADD ./entrypoint.sh /entrypoint.sh
ADD . /careplus

RUN pip install -r requirements.txt

RUN groupadd -r django && useradd -r -g django django

RUN chown -R django /careplus && chmod +x entrypoint.sh && chown django entrypoint.sh

WORKDIR /careplus

ENTRYPOINT ["/entrypoint.sh"]

FROM python:3.5
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /requirements.txt
ADD ./entrypoint.sh /entrypoint.sh
ADD . /careplus

RUN pip install -r requirements.txt

RUN groupadd -r django && useradd -r -g django django

RUN chown -R django /careplus && chmod +x entrypoint.sh && chown django entrypoint.sh

WORKDIR /careplus

ENTRYPOINT ["/entrypoint.sh"]

