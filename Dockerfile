FROM python:3.8-alpine AS base

WORKDIR /oxygen-cs-grp01-eq6
COPY Pipfile Pipfile.lock /oxygen-cs-grp01-eq6/

RUN pip install pipenv
RUN pipenv install --deploy
RUN pip cache purge
RUN rm -rf /root/.cache/*

CMD ["pipenv", "run", "start"]
