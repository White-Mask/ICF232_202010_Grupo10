FROM python:3.7

ENV DJANGO_SETTINGS_MODULE SigVip.production

ENV PYTHONUNBUFFERED 1

RUN mkdir SigVip

WORKDIR /SigVip

ADD . /SigVip

RUN ./setup.sh

ENTRYPOINT ["./start.sh"]

EXPOSE 80