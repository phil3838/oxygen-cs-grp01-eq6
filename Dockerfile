FROM python:3.8-slim

WORKDIR /oxygen-cs-grp01-eq6

COPY Pipfile Pipfile.lock /oxygen-cs-grp01-eq6/

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . /oxygen-cs-grp01-eq6

CMD ["pipenv", "run", "start"]